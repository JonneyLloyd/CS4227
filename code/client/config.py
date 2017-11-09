from os import environ

from framework.server.config import ServerConfig


class ProdConfig(ServerConfig):
    DATABASE_URI = ''
    DATABASE_KEY = ''


class DevConfig(ServerConfig):
    APP_PORT = 8080
    DEBUG = True
    LOG_LEVEL = 'verbose'
    DATABASE_URI = ''
    DATABASE_KEY = ''
    environ['AWS_ACCESS_KEY_ID'] = 'dummy'
    environ['AWS_SECRET_ACCESS_KEY'] = 'dummy'
    AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
    DYNAMO_ENABLE_LOCAL = True
    DYNAMO_LOCAL_HOST = 'localhost'
    DYNAMO_LOCAL_PORT = 8000
    DYNAMO_TABLES = [
        dict(
            TableName='mementos',
            KeySchema=[dict(AttributeName='type', KeyType='HASH')],
            AttributeDefinitions=[dict(AttributeName='type', AttributeType='S')],
            ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5),
        )
    ]


class TestConfig(ServerConfig):
    APP_PORT = 5000
    DEBUG = True
    LOG_LEVEL = 'debug'
    DATABASE_URI = ''
    DATABASE_KEY = ''
    environ['AWS_ACCESS_KEY_ID'] = 'dummy'
    environ['AWS_SECRET_ACCESS_KEY'] = 'dummy'
    AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
    DYNAMO_ENABLE_LOCAL = True
    DYNAMO_LOCAL_HOST = 'localhost'
    DYNAMO_LOCAL_PORT = 8000
    DYNAMO_TABLES = [
        dict(
            TableName='mementos',
            KeySchema=[dict(AttributeName='type', KeyType='HASH')],
            AttributeDefinitions=[dict(AttributeName='type', AttributeType='S')],
            ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5),
        )
    ]
