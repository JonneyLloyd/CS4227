import unittest
from typing import List, Mapping, Deque, Dict
from framework.config import ConfigModel, ConfigMemento, attribute_property
from .demo_util import ChildConfig, ParentConfig

class TestConfigModel(unittest.TestCase):

    def test_create_memento(self):
        c = ChildConfig()
        c.numbers = [1, 2, 3]
        memento = c.create_memento()
        self.assertEqual(memento.config, {'child_config': {'numbers': [1, 2, 3]},  'concrete_key': 'child_config'})

    def test_create_memento_nested(self):
        p = ParentConfig()
        p.a = 'word'
        p.child = ChildConfig()
        p.child.numbers = [1, 2, 3]
        memento = p.create_memento()
        self.assertEqual(memento.config, {'parent': {'child': {'numbers': [1, 2, 3]}, 'amazing': 'word'}, 'concrete_key': 'parent'})

    def test_set_memento(self):
        memento = ConfigMemento()
        memento.config = {'child_config': {'numbers': [1, 2, 3]}, 'concrete_key': 'child_config'}
        c = ChildConfig()
        c.set_memento(memento)
        self.assertEqual(c.create_memento().config, memento.config)

    def test_set_memento_nested(self):
        memento = ConfigMemento()
        memento.config = {'parent': {'child': {'numbers': [1, 2, 3]}, 'amazing': 'word'}, 'concrete_key': 'parent'}
        p = ParentConfig()
        p.set_memento(memento)
        self.assertEqual(p.create_memento().config, memento.config)

    def test_create_schema(self):
        schema = ChildConfig.create_schema()
        self.assertEqual(
            schema,
            {
                'documentname': 'child_config',
                'type': 'object',
                'properties': {
                    'numbers': {
                        'type': 'object',
                        'ref': 'definitions/list[integer]'
                    }
                },
                'definitions': {
                    'list[integer]': {
                        'type': 'list', 'type_params': ['integer']
                    }
                }
            }
        )

    def test_create_schema_nested(self):
        schema = ParentConfig.create_schema()
        self.assertEqual(
            schema,
            {
                'documentname': 'parent',
                'type': 'object',
                'properties': {
                    'child': {
                        'type': 'object',
                        'ref': 'definitions/child_config'
                    },
                    'amazing': {
                        'type': 'string'
                    }
                },
                'required': ['child', 'amazing'],
                'definitions': {
                    'child_config': {
                        'documentname': 'child_config',
                        'type': 'object',
                        'properties': {
                            'numbers': {
                                'type': 'object',
                                'ref': 'definitions/list[integer]'
                            }
                        },
                        'definitions': {
                            'list[integer]': {
                                'type': 'list',
                                'type_params': ['integer']
                            }
                        }
                    }
                }
            }
        )
