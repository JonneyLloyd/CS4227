from config_interface import ConfigInterface
from os import environ


class Config(ConfigInterface):

    def __init__(self, mode: str) -> None:
        if mode == 'debug':
            self._create_debug_config()
        elif mode == 'dev':
            self._create_debug_config()
        elif mode == 'prod':
            ...
        else:
            raise Exception(f"Unknown mode: {mode}")
        self.DYNAMO_TABLES = [
            self._create_table('mementos', 'id', 'S')
        ]

    def _create_debug_config(self) -> None:
        environ['AWS_ACCESS_KEY_ID'] = 'dummy'
        environ['AWS_SECRET_ACCESS_KEY'] = 'dummy'
        self.AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
        self.AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
        self.DYNAMO_ENABLE_LOCAL = True
        self.DYNAMO_LOCAL_HOST = 'localhost'
        self.DYNAMO_LOCAL_PORT = 8000

    def _create_table(self, table_name, name, _type) -> dict:
        return dict(
            TableName=table_name,
            KeySchema=[dict(AttributeName=name, KeyType='HASH')],
            AttributeDefinitions=[dict(AttributeName=name, AttributeType=_type)],
            ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5),
        )
