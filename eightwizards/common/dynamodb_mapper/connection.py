import logging
import boto3
from django.conf import settings

log = logging.getLogger(__name__)
dblog = logging.getLogger(__name__+".database-access")


class DynamoDBConnection:
    """Connection that handles access to DynamoDB.

    You should never make any explicit/direct ``boto.dynamodb`` calls by yourself
    except for table maintenance operations :

        - ``boto.dynamodb.table.update_throughput()``
        - ``boto.dynamodb.table.delete()``

    Remember
    _connection_settings is map for potential boto3.Session params
            - region_name
            - api_version
            - use_ssl
            - verify
            - endpoint_urls
            - aws_access_key_id
            - aws_secret_access_key
            - aws_session_token,
            - config

    Singleton
    """

    class ConnectionBorg:

        DEFAULT_REGION = 'us-west-1'

        _connection_settings = {}

        _resource_connection = None

        def __init__(self, connection_settings=None):
            # TODO: perhaps we need a simple validation there. Basic realization did not had it
            if connection_settings:
                self._connection_settings = connection_settings
            else:
                self._connection_settings = getattr(settings, 'DYNAMODB')
            if not self._connection_settings.get('region_name'):
                self._connection_settings['region_name'] = self.DEFAULT_REGION

        @property
        def resource(self):
            return self._get_resource_connection()

        def _get_resource_connection(self):
            """Return the DynamoDB connection for the mapper as resource
            """
            dblog.debug('connection_settings: - %s', self._connection_settings)
            if self._resource_connection is None:
                self._resource_connection = boto3.resource('dynamodb', **self._connection_settings)
            return self._resource_connection

    instance = None

    def __new__(cls, connection_settings=None):
        if not DynamoDBConnection.instance:
            DynamoDBConnection.instance = DynamoDBConnection.ConnectionBorg(connection_settings)
        return DynamoDBConnection.instance

    def __init__(self):
        pass

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
