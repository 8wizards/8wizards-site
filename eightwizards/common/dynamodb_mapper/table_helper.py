import logging
from django.conf import settings
from botocore.exceptions import ClientError
from .errors import ValidationError, SchemaError
from .connection import DynamoDBConnection

log = logging.getLogger(__name__)
dblog = logging.getLogger(__name__+".database-access")

KEY_TYPE_HASH = 'HASH'
KEY_TYPE_RANGE = 'RANGE'


class TableHelper(object):
    _tables_cache = {}

    @staticmethod
    def get_environment():
        """
        Returns application environment name - needs per kind of table namespace
        :return: string
        """
        return getattr(settings, 'ENVIRONMENT_NAME', 'arena')

    @staticmethod
    def create_table(cls_model):
        """Create a table that'll be used to store instances of cls_model.

        See `Amazon's developer guide <http://docs.amazonwebservices.com/amazondynamodb/latest/developerguide/
        ProvisionedThroughputIntro.html>`_
        for more information about provisioned throughput.

        """

        conn = DynamoDBConnection().resource
        if TableHelper.is_table_existed(TableHelper.get_env_table_name(cls_model.__table__)):
            return TableHelper.get_table(cls_model.__table__)

        create_config = TableHelper.prepare_create_table_config(cls_model)

        try:
            table = conn.create_table(**create_config)
            return table
        except ClientError as e:
            if e.response['Error']['Code'] == 'ValidationException':
                raise ValidationError(e)
            else:
                log.error(e)
                raise

    @staticmethod
    def update_table(cls_model):
        """Updates table configuration by model's class schema

        TODO: Need muck more work to compare and make proper update - for global indexes it's not regular
        """
        if TableHelper.is_table_existed(TableHelper.get_env_table_name(cls_model.__table__)):

            table = TableHelper.get_table(cls_model.__table__)
            dblog.info('Received table=%s', table)
            # Need muck more work to compare and make proper update - for global indexes it's not regular

    @staticmethod
    def delete_table(table):
        """Deletes table
        """

        if getattr(table, '__table__', None):
            name = table.__table__
        elif isinstance(table, str):
            name = table
        else:
            raise ValidationError('Wrong table name - table=%s' % table)

        table = TableHelper.get_table(name)

        dblog.debug("Clearing tables cache per connection")
        try:
            del TableHelper._tables_cache[table.name]
        except KeyError:
            dblog.error("Table '%s' is not in cache", name)

        try:
            return table.delete()
        except ClientError as e:
            dblog.error('delete_table - %s', e)
            return None

    @staticmethod
    def refresh_table(name):
        name = TableHelper.get_env_table_name(name)

        try:
            table = DynamoDBConnection().resource.Table(name)
            TableHelper._tables_cache[name] = table

            return table
        except ClientError as ex:
            dblog.error('DynamoDB refreshing table issue - %s', ex)
            return None

    @staticmethod
    def get_table(name):
        """Return the table with the requested name."""
        name = TableHelper.get_env_table_name(name)
        if name not in TableHelper._tables_cache:
            try:
                TableHelper._tables_cache[name] = DynamoDBConnection().resource.Table(name)
            except ClientError as ex:
                dblog.error('DynamoDB getting table issue - %s', ex)

        return TableHelper._tables_cache.get(name)

    ENV_TABLE_NAME_FORMAT = '{env}_{name}'

    @staticmethod
    def get_env_table_name(name):
        return TableHelper.ENV_TABLE_NAME_FORMAT.format(env=TableHelper.get_environment(), name=name)

    @staticmethod
    def is_table_existed(name_witn_env):
        """
        Checks is table has been already created/preexisted/ready to use

        :param name_witn_env: table name with env prefix
        :return: table status or False
        """
        table = DynamoDBConnection().resource.Table(name_witn_env)
        try:
            return table.table_status
        except ClientError as ex:
            dblog.error('DynamoDB getting table status issue - %s', ex)
            return False

    @staticmethod
    def prepare_create_table_config(cls_model):
        """
        Bakes structured schema config based on model's schema

        :param cls_model: DynamoDB class
        :return: dict - table structure dict
        """
        table_name = TableHelper.get_env_table_name(cls_model.__table__)
        hash_key_name = cls_model.__hash_key__
        range_key_name = cls_model.__range_key__

        if not table_name:
            raise SchemaError("Class does not define __table__", cls_model)

        # FIXME: check key is defined in schema
        if not hash_key_name:
            raise SchemaError("Class does not define __hash_key__", cls_model)

        if not cls_model.__schema__:
            raise SchemaError("Class does not define __schema__", cls_model)

        key_schema = list()

        # It's a prototype/an instance, not a type.
        # None in the case of a hash-only table.
        key_schema.append({
            'AttributeName': hash_key_name,
            'KeyType': KEY_TYPE_HASH
        })
        if range_key_name:
            key_schema.append({
                'AttributeName': range_key_name,
                'KeyType': KEY_TYPE_RANGE
            })

        # IMPORTANT: Populate basic create table config
        create_config = {
            'KeySchema': key_schema,
            'TableName': table_name,
            'ProvisionedThroughput': {
                'ReadCapacityUnits': cls_model.__read_units__,
                'WriteCapacityUnits': cls_model.__write_units__
            }
        }

        needed_attributes_fields = {hash_key_name, range_key_name}

        # create local indexes structures
        if cls_model.__local_indexes__:
            local_indexes = TableHelper.prepare_index_stucture(cls_model, is_global=False)

            if local_indexes:
                create_config['LocalSecondaryIndexes'] = local_indexes # IMPORTANT: Populate Local Secondary Indexes

                for item in local_indexes:
                    for key in item.get('KeySchema'):
                        needed_attributes_fields.add(key['AttributeName'])

        # create local indexes structures
        if cls_model.__global_indexes__:
            global_indexes = TableHelper.prepare_index_stucture(cls_model, is_global=True)
            if global_indexes:
                create_config['GlobalSecondaryIndexes'] = global_indexes  # IMPORTANT: Populate Global Secondary Indexes

                for item in global_indexes:
                    for key in item.get('KeySchema'):
                        needed_attributes_fields.add(key['AttributeName'])

        attributes = []
        for item, item_type in cls_model.__schema__.items():
            if item in needed_attributes_fields:
                attributes.append({
                    'AttributeName': item,
                    'AttributeType': item_type
                })
        create_config['AttributeDefinitions'] = attributes  # IMPORTANT: Populate Attributes

        return create_config

    @staticmethod
    def prepare_index_stucture(cls_model, is_global=False):
        """
        Creates local or global index structure according to the DynamoDB documentation
        TODO: I don't like acess to cls structure via CONSTS - perhaps need to have some properties or accessors
        :param cls_model:  DynamoDBModel class to create
        :param is_global: is global index indicator
        :return:
        """
        indexes = []
        indexes_schema = cls_model.__global_indexes__ if is_global else cls_model.__local_indexes__
        for index_name, config in indexes_schema.items():
            # pre-validate at least schema structure
            if cls_model.validate_indexes(config):
                projection_cfg = {
                    'ProjectionType': config.get(cls_model.REQUIRED_PROJECTION_TYPE_PARAM)
                }

                if config.get('non_key_attributes'):
                    projection_cfg['NonKeyAttributes'] = config.get('non_key_attributes')
                db_config = {
                    'IndexName': index_name,
                    'KeySchema': [
                        {
                            'AttributeName': config.get(cls_model.REQUIRED_KEY_SCHEMA_PARAM).get(key_type),
                            'KeyType': 'HASH' if key_type == cls_model.REQUIRED_KEY_SCHEMA_HASH else 'RANGE'
                        } for key_type in sorted(config.get(cls_model.REQUIRED_KEY_SCHEMA_PARAM).keys())
                        ],
                    'Projection': projection_cfg
                }
                if is_global:
                    db_config['ProvisionedThroughput'] = {
                        'ReadCapacityUnits': config.get('read_units') if config.get('read_units')
                        else cls_model.__read_units__,
                        'WriteCapacityUnits': config.get('writes_units') if config.get('writes_units')
                        else cls_model.__write_units__
                    }
                indexes.append(db_config)
        return indexes
