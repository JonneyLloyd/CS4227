import unittest

from framework.config import ConfigModel, attribute_property


class TestAttributeProperty(unittest.TestCase):

    def test_attribute_access(self):
        class Test(ConfigModel):

            def __init__(self, value: str=None) -> None:
                self._value = value

            @attribute_property('value_name')
            def value(self) -> str:
                return self._value

            @value.setter
            def value(self, value: str) -> None:
                self._value = value


        t = Test()
        self.assertEqual(t.value, None)
        t.value = 'testing'
        self.assertEqual(t.value, 'testing')
        self.assertEqual(Test.value.name, 'value_name')
        self.assertEqual(Test.value.required, True)
