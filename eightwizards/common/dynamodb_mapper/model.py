# pylint: disable=all

"""Object mapper for Amazon DynamoDB.

Based in part on mongokit's Document interface.

Released under the GNU LGPL, version 3 or later (see COPYING).
"""
from __future__ import absolute_import

import logging
import copy
from boto3.exceptions import DynamoDBNeedsKeyConditionError
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr, Key
from .schema import Schema
from .connection import DynamoDBConnection
from .table_helper import TableHelper
from .errors import ValidationError, OverwriteError, ConflictError, ResourceNotFoundError

log = logging.getLogger(__name__)
dblog = logging.getLogger(__name__+".database-access")


class DynamoDBModel(object):
    """Abstract base class for all models that use DynamoDB as their storage
    backend.

    Each subclass must define the following attributes:

      - ``__table__``: the name of the table used for storage.
      - ``__hash_key__``: the name of the primary hash key.
      - ``__range_key__``: (optional) if you're using a composite primary key,
          the name of the range key.
      - ``__schema__``: ``{attribute_name: attribute_type}`` mapping.
          Supported attribute_types are: int, long, float, str, unicode, set.
          Default values are obtained by calling the type with no args
          (so 0 for numbers, "" for strings and empty sets).
      - ``__defaults__``: (optional) ``{attribute_name: defaulter}`` mapping.
          This dict allows to provide a default value for each attribute_name at
          object creation time. It will *never* be used when loading from the DB.
          It is fully optional. If no value is supplied the empty value
          corresponding to the type will be used.
          "defaulter" may either be a scalar value or a callable with no
          arguments.
      - ``__migrator__``: :py:class:`~.Migration` handler attached to this model

    To redefine serialization/deserialization semantics (e.g. to have more
    complex schemas, like auto-serialized JSON data structures), override the
    _from_dict (deserialization) and _to_db_dict (serialization) methods.

    *Important implementation note regarding sets:* DynamoDB can't store empty
    sets/strings. Therefore, since we have schema information available to us,
    we're storing empty sets/strings as missing attributes in DynamoDB, and
    converting back and forth based on the schema.

    So if your schema looks like the following::

        {
            "id": unicode,
            "name": str,
            "cheats": set
        }

    then::

        {
            "id": "e1m1",
            "name": "Hangar",
            "cheats": set([
                "idkfa",
                "iddqd"
            ])
        }

    will be stored exactly as is, but::

        {
            "id": "e1m2",
            "name": "",
            "cheats": set()
        }

    will be stored as simply::

        {
            "id": "e1m2"
        }
    """
    MAX_INDEX_NUMBER = 5

    PROJECTION_TYPE_KEYS_ONLY = 'KEYS_ONLY'
    PROJECTION_TYPE_ALL = 'ALL'
    PROJECTION_TYPE_INCLUDE = 'INCLUDE'

    DEFAULT_PROJECTION_TYPE = PROJECTION_TYPE_ALL

    ALLOWED_PROJECTION_TYPE = (PROJECTION_TYPE_KEYS_ONLY, PROJECTION_TYPE_INCLUDE, PROJECTION_TYPE_ALL)

    REQUIRED_PROJECTION_TYPE_PARAM = 'projection_type'
    REQUIRED_KEY_SCHEMA_PARAM = 'key_schema'

    REQUIRED_KEY_SCHEMA_HASH = 'hash_key'
    REQUIRED_KEY_SCHEMA_RANGE = 'range_key'

    INDEXES_REQUIRES = (REQUIRED_KEY_SCHEMA_PARAM, REQUIRED_PROJECTION_TYPE_PARAM)

    # TODO Add checks to the various methods so that meaningful error messages
    # are raised when they're incorrectly overridden.
    __table__ = None
    __hash_key__ = None
    __range_key__ = None
    __schema__ = {}
    __migrator__ = None
    __local_indexes__ = None
    __global_indexes__ = None

    __read_units__ = 5
    __write_unites__ = 5

    __defaults__ = {}

    def __init__(self, **kwargs):
        """Create an instance of the model. All fields defined in the schema
        are created. By order of priority its value will be loaded from:

            - kwargs
            - __defaults__
            - None. Warning, this will most likely cause failures at save time

        We're supplying this method to avoid the need for extra checks in save and
        ease object initial creation.

        Objects created and initialized with this method are considered as not
        coming from the DB.
        """
        cls = type(self)
        defaults = cls.__defaults__
        schema = cls.__schema__

        self._raw_data = {}

        for (name, type_) in schema.items():
            if name in kwargs:
                value = kwargs.get(name)
            elif name in defaults:
                template = defaults[name]
                if callable(template):
                    value = template()
                else:
                    value = copy.deepcopy(template)
            else:
                value = None
            setattr(self, name, value)

        # instanciate the migrator only once per model *after* initialization
        # as it assumes a fully initialized model
        if isinstance(cls.__migrator__, type):
            cls.__migrator__ = cls.__migrator__(cls)

    def __repr__(self):
        """
        Instance representation
        :return: str
        """
        if self.__range_key__:
            return '<{cls} {hash}={hash_value}, {range}={range_value}>'.format(
                cls=self.__class__.__name__,
                hash=self.__hash_key__,
                range=self.__range_key__,
                hash_value=getattr(self, self.__hash_key__, 'N/A'),
                range_value=getattr(self, self.__range_key__, 'N/A')
            )
        return '<{cls} {hash}={hash_value}>'.format(
                cls=self.__class__.__name__,
                hash=self.__hash_key__,
                range=self.__range_key__,
                hash_value=getattr(self, self.__hash_key__, 'N/A')
        )

    def __unicode__(self):
        """
        Instance representation
        :return: str
        """
        return self.__repr__()

    def validate(self):
        """Return a ``dict`` of validated fields if validators passes. Otherwise
        ``InvalidList`` is raised.
        """
        # load schema
        schema = self.__schema__
        validate = Schema(schema)
        # load schema data from self
        data = {str(key): getattr(self, str(key)) for key in schema}
        # return validated data (or raise)
        return validate(data)

    @classmethod
    def get(cls, hash_key_value, range_key_value=None):
        """Retrieve a single object from DynamoDB according to its primary key.

        Note that this is not a query method -- it will only return the object
        matching the exact primary key provided. Meaning that if the table is
        using a composite primary key, you need to specify both the hash and
        range key values.

        Objects loaded by this method are marked as coming from the DB. Hence
        their initial state is saved in ``self._raw_data``.

        :param hash_key_value: The value of the requested item's hash_key.

        :param range_key_value: The value of the requested item's range_key,
            if the table has a composite key.

        """
        table = TableHelper.get_table(cls.__table__)
        key_struct = {
            cls.__hash_key__: hash_key_value
        }
        if cls.__range_key__ and range_key_value:
            key_struct[cls.__range_key__] = range_key_value

        try:
            item = table.get_item(Key=key_struct)
            dblog.info("Got item (%s, %s) from table %s", hash_key_value, range_key_value, cls.__table__)
            return cls._from_db_dict(item.get('Item', {})) if item.get('Item', {}) else None
        except ClientError as e:
            if e.response['Error']['Code'] == 'ValidationException':
                raise ValidationError(e)
            else:
                log.error(e)
                raise

    @classmethod
    def get_batch(cls, keys):
        """Retrieve multiple objects according to their primary keys.

        Like get, this isn't a query method -- you need to provide the exact
        primary key(s) for each object you want to retrieve:

          - If the primary keys are hash keys, keys must be a list of
            their values (e.g. ``[1, 2, 3, 4]``).
          - If the primary keys are composite (hash + range), keys must
            be a list of ``(hash_key, range_key)`` values
            (e.g. ``[("user1", 1), ("user1", 2), ("user1", 3)]``).

        get_batch *always* performs eventually consistent reads.

        Objects loaded by this method are marked as coming from the DB. Hence
        their initial state is saved in ``self._raw_data``.

        :param keys: iterable of keys. ex ``[(hash1, range1), (hash2, range2)]``

        """

        # Convert all the keys to DynamoDB values.
        if cls.__range_key__:
            dynamo_keys = [
                {cls.__hash_key__: h,
                 cls.__range_key__: r}
                for (h, r) in keys
            ]
        else:
            dynamo_keys = [{cls.__hash_key__: h} for h in keys]
        try:
            res = DynamoDBConnection().resource.batch_get_item(RequestItems={
                TableHelper.get_env_table_name(cls.__table__): {
                    'Keys': dynamo_keys
                }
            })
            dblog.debug("Sent a batch get on table %s", cls.__table__)
            return [cls._from_db_dict(d) for d in res.get('Responses', {}).get(
                TableHelper.get_env_table_name(cls.__table__), [])]

        except ClientError as e:
            if e.response['Error']['Code'] == 'ValidationException':
                raise ValidationError(e)
            else:
                log.error(e)
                raise

    @classmethod
    def query(cls, hash_key_value, search_expression, consistent_read=False, reverse=False, limit=None, index=None,
              last=None,**kwargs):
        """Query DynamoDB for items matching the requested key criteria.

        You need to supply an exact hash key value, and optionally, conditions
        on the range key. If no such conditions are supplied, all items matching
        the hash key value will be returned.

        This method can only be used on tables with composite (hash + range)
        primary keys -- since the exact hash key value is mandatory, on tables
        with hash-only primary keys.

        Objects loaded by this method are marked as coming from the DB. Hence
        their initial state is saved in ``self._raw_data``.

        :param hash_key_value: The hash key's value for all requested items.

        :param search_expression: A condition string for a range key condition
            Expression condition class from boto3.dynamodb.conditions
            from boto3.dynamodb.conditions import Key, Attr
            Key per RANGE HASH
            Attr per secondary indexes

        :param consistent_read: If False (default), an eventually consistent
            read is performed. Set to True for strongly consistent reads.

        :param reverse: Ask DynamoDB to scan the ``range_key`` in the reverse
            order. For example, if you use dates here, the more recent element
            will be returned first. Defaults to ``False``.

        :param limit: Specify the maximum number of items to read from the table.t
            Even though Boto returns a generator, it works by batchs of 1MB.
            using this option may help to spare some read credits. Def`lts to
            ``None``

        :param index: Specify the search index name, defaults to ``None``

        :param last: Specify last evaluated key for pagination, defaults to ``None``

        :param kwargs: Extra requests

        :rtype: (generator, last evaluated key)
        """

        table = TableHelper.get_table(cls.__table__)

        from .conditions import Key
        query_params = {
            'TableName': table.name,
            'ConsistentRead': consistent_read,
            'ScanIndexForward': not reverse,
            'KeyConditionExpression': Key(cls.__hash_key__).eq(hash_key_value) & search_expression
        }
        if limit:
            query_params['Limit'] = int(limit)
        if index:
            query_params['IndexName'] = index

        if last:
            query_params['ExclusiveStartKey'] = last

        query_params.update(kwargs)

        try:
            res = table.query(**query_params)
            return [cls._from_db_dict(d) for d in res.get('Items', []) if d], res.get('LastEvaluatedKey')
        except ClientError as e:
            if e.response['Error']['Code'] == 'ValidationException':
                raise ValidationError(e)
            else:
                log.error(e)
                raise

    @classmethod
    def scan(cls, search_expression, consistent_read=False, limit=None, index=None, last=None, **kwargs):
        """Scan DynamoDB for items matching the requested criteria.

        You can scan based on any attribute and any criteria (including multiple
        criteria on multiple attributes), not just the primary keys.

        Scan is a very expensive operation -- it doesn't use any indexes and will
        look through the entire table. As much as possible, you should avoid it.

        Objects loaded by this method are marked as coming from the DB. Hence
        their initial state is saved in ``self._raw_data``.

        :param search_expression: A condition string for a range key condition
            Expression condition class from boto3.dynamodb.conditions
            from boto3.dynamodb.conditions import Key, Attr
            Key per RANGE HASH
            Attr per secondary indexes

        :param consistent_read: If False (default), an eventually consistent
            read is performed. Set to True for strongly consistent reads.

        :param limit: Specify the maximum number of items to read from the table.t
            Even though Boto returns a generator, it works by batchs of 1MB.
            using this option may help to spare some read credits. Def`lts to
            ``None``

        :param index: Specify the search index name, defaults to ``None``

        :param last: Specify last evaluated key for pagination, defaults to ``None``

        :param kwargs: Extra requests

        :rtype: (generator, last evaluated key)
        """

        table = TableHelper.get_table(cls.__table__)

        scan_params = {
            'TableName': table.name,
            'ConsistentRead': consistent_read,
            'FilterExpression': search_expression
        }
        if limit:
            scan_params['Limit'] = int(limit)
        if index:
            scan_params['IndexName'] = index

        if last:
            scan_params['ExclusiveStartKey'] = last

        scan_params.update(kwargs)

        try:
            res = table.scan(**scan_params)
            return [cls._from_db_dict(d) for d in res.get('Items', []) if d], res.get('LastEvaluatedKey')
        except ClientError as e:
            if e.response['Error']['Code'] == 'ValidationException':
                raise ValidationError(e)
            else:
                log.error(e)
                raise

    @classmethod
    def validate_indexes(cls, indexes_structure):
        """ Pre-Validates local or global structure params

        TODO: Not good styled code - constants are not usual practice on this class.

        :param indexes_structure:
        :return: bool
        """
        requires = list(cls.INDEXES_REQUIRES)
        for key in indexes_structure.keys():
            try:
                requires.pop(requires.index(key))
            except ValueError:
                continue

        if requires:
            raise ValidationError('Not enough params in the index configuration: need to add %s', requires)

        if not indexes_structure.get(cls.REQUIRED_KEY_SCHEMA_PARAM) and \
            cls.REQUIRED_KEY_SCHEMA_HASH not in indexes_structure.get(cls.REQUIRED_KEY_SCHEMA_PARAM) and \
                cls.REQUIRED_KEY_SCHEMA_RANGE not in indexes_structure.get(cls.REQUIRED_KEY_SCHEMA_PARAM):

            msg = '%s must contain %s or %s fields' % (cls.REQUIRED_KEY_SCHEMA_PARAM,
                                                       cls.REQUIRED_KEY_SCHEMA_HASH, cls.REQUIRED_KEY_SCHEMA_RANGE)
            raise ValidationError(msg)

        hash_field = indexes_structure.get(cls.REQUIRED_KEY_SCHEMA_PARAM).get(cls.REQUIRED_KEY_SCHEMA_HASH)
        range_field = indexes_structure.get(cls.REQUIRED_KEY_SCHEMA_PARAM).get(cls.REQUIRED_KEY_SCHEMA_RANGE)

        if hash_field == range_field:
            raise ValidationError('Index range key cannot be the same as the index hash key')

        if hash_field not in cls.__schema__.keys():
            raise ValidationError('Hash Key must be a schema attribute')

        if range_field and range_field not in cls.__schema__.keys():
            raise ValidationError('Range Key must be a schema attribute')
        return True

    @classmethod
    def _from_db_dict(cls, raw_data):
        """Build an instance from a dict-like mapping, according to the class's
        schema. Objects created with this method are considered as comming from
        the DB. The initial state is persisted in ``self._raw_data``.
        If a ``__migrator__`` has been declared, migration is triggered on a copy
        of the raw data.

        Default values are used for anything that's missing from the dict
        (see DynamoDBModel class docstring).
        Direct use of this method should be avoided as much as possible but still
        may be usefull for "deep copy".

        Overload this method if you need a special (de-)serialization semantic

        :param raw_data: Raw db dict

        """
        # FIXME: type check. moving to __init__ syntax may break some implementations

        instance = cls()
        instance._raw_data = raw_data

        # If a migrator is registered, trigger it
        if cls.__migrator__ is not None:
           raw_data = cls.__migrator__(raw_data)

        # de-serialize data
        for (name, type_) in cls.__schema__.items():
            # Set the value if we got one from DynamoDB. Otherwise, stick with the default
            value = raw_data.get(name)    # de-serialize
            setattr(instance, name, value)

        return instance

    def _to_db_dict(self):
        """Return a dict representation of the object according to the class's
        schema, suitable for direct storage in DynamoDB.

        Direct use of this method should be avoided as much as possible but still
        may be useful for "deep copy".

        Overload this method if you need a special serialization semantic
        """
        data = self.validate()
        return {key: val for key, val in data.items() if val or val == 0}

    def save(self, raise_on_conflict=False):
        """Save the object to the database.

        This method may be used both to insert a new object in the DB, or to
        update an existing one (iff ``raise_on_conflict == False``).

        It also embeds the high level logic to avoid the 'lost update' syndrom.
        Internally, it uses ``expected_values`` set to ``self._raw_data``

        ``raise_on_conflict=True`` scenarios:

        - **object from database**: Use ``self._raw_dict`` to generate ``expected_values``
        - **new object**: ``self._raw_dict`` is empty, set ``allow_overwrite=True``
        - **new object with autoinc**: flag has no effect
        - **(accidentally) editing keys**: Use ``self._raw_dict`` to generate ``expected_values``,
        will catch overwrites and insertion to empty location

        :param raise_on_conflict: flag to toggle overwrite protection -- if any
            one of the original values doesn't match what is in the database
            (i.e. someone went ahead and modified the object in the DB behind
            your back), the operation fails and raises
            :class:`ConflictError` or ``OverwriteError``.

        :raise ConflictError: Target object has changed between read and write operation
        :raise OverwriteError: A new Item overwrites an existing one and ``raise_on_conflict=True``.
        :raise ResourceNotFoundError: A new Item is putting to non existing table.
         Note: this exception inherits from ConflictError
        """

        cls = type(self)
        allow_overwrite = True
        schema = cls.__schema__
        hash_key = cls.__hash_key__
        range_key = cls.__range_key__

        condition_expressions = None

        table = TableHelper.get_table(cls.__table__)
        item_data = self._to_db_dict()

        # Regular save
        if raise_on_conflict:
            if self._raw_data:
                # Empty strings/sets must be represented as missing values
                for name in schema.keys():
                    if name not in self._raw_data:
                        attr_or_key = Key if name in (cls.__hash_key__, cls.__range_key__) else Attr
                        if condition_expressions is None:
                            condition_expressions = attr_or_key(name).eq(self._raw_data.get(name))
                        else:
                            condition_expressions &= attr_or_key(name).eq(self._raw_data.get(name))
            else:
                # Forbid overwrites: do a conditional write on
                # "this hash_key doesn't exist"
                allow_overwrite = False

        put_params = {
            'Item': item_data
        }

        if allow_overwrite and condition_expressions:
            put_params['ConditionExpression'] = condition_expressions

        try:
            table.put_item(**put_params)
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                if allow_overwrite:
                    # Conflict detected
                    raise ConflictError(item_data)
                    # Forbidden overwrite
                raise OverwriteError(item_data)
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise ResourceNotFoundError(e)
            else:
                log.error(e)
                raise  # raise generic exception too
        except Exception as e:
            log.error(e)
            raise

        # Update Raw_data to reflect DB state on success
        self._raw_data = item_data

        hash_key_value = getattr(self, hash_key)
        range_key_value = getattr(self, range_key, None) if range_key else None
        dblog.debug("Saved (%s, %s) in table %s raise_on_conflict=%s", hash_key_value, range_key_value, cls.__table__,
                    raise_on_conflict)

    def delete(self, raise_on_conflict=False):
        """Delete the current object from the database.

        If the Item has been edited before the ``delete`` command is issued and
        ``raise_on_conflict=True`` then, :class:`ConflictError` is raised.

        :param raise_on_conflict: flag to toggle overwrite protection -- if any
            one of the original values doesn't match what is in the database
            (i.e. someone went ahead and modified the object in the DB behind
            your back), the operation fails and raises
            :class:`ConflictError`.

        :raise ConflictError: Target object has changed between read and write operation
        """
        cls = type(self)
        schema = cls.__schema__
        hash_key_value = getattr(self, cls.__hash_key__)
        h_value = hash_key_value

        condition_expressions = None

        if raise_on_conflict:
            if self._raw_data:
                # Empty strings/sets must be represented as missing values
                for name in schema.keys():
                    if name not in self._raw_data:
                        attr_or_key = Key if name in (cls.__hash_key__, cls.__range_key__) else Attr
                        if condition_expressions is None:
                            condition_expressions = attr_or_key(name).eq(self._raw_data.get(name))
                        else:
                            condition_expressions &= attr_or_key(name).eq(self._raw_data.get(name))
            else:  # shortcut :D
                raise ConflictError("Attempts to delete an object which has not yet been persited with raise_on"
                                    "_conflict=True")

        delete_keys = {
            cls.__hash_key__: h_value,
        }

        # Range key is only present in composite primary keys
        range_key_value = None
        if cls.__range_key__:
            range_key_value = getattr(self, cls.__range_key__)
            delete_keys[cls.__range_key__] = range_key_value

        delete_params = {
            'Key': delete_keys,
        }
        if condition_expressions:
                delete_params['ConditionExpression'] = condition_expressions

        try:
            table = TableHelper.get_table(cls.__table__)
            table.delete_item(**delete_params)
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                if allow_overwrite:
                    # Conflict detected
                    raise ConflictError(item_data)
                    # Forbidden overwrite
                raise OverwriteError(item_data)
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise ResourceNotFoundError(e)
            else:
                log.error(e)
                raise  # raise generic exception too
        except Exception as e:
            log.error(e)
            raise

        # Make sure any further save will be considered as *insertion*
        self._raw_data = {}

        dblog.debug("Deleted (%s, %s) from table %s", h_value, range_key_value, cls.__table__)
