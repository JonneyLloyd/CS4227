import unittest
from typing import List, Dict
from abc import ABC, abstractmethod

from framework.util.overload import overload, registry_test_context


class A():
    ...


class B(A):
    ...


class C(A):
    ...


class D(C):
    ...


class TestOverloadDecorator(unittest.TestCase):

    def test_overload_concrete(self):
        with registry_test_context():
            class Test():

                @overload
                def test(self, t: B) -> str:
                    return 'B'

                @overload
                def test(self, t: C) -> str:
                    return 'C'


            x = Test()
            self.assertEqual(x.test(B()), 'B')
            self.assertEqual(x.test(C()), 'C')

    def test_overload_interface(self):
        with registry_test_context():
            class Test():

                @overload
                def test(self, t: B) -> str:
                    return 'B'

                @overload
                def test(self, t: C) -> str:
                    return 'C'


            x = Test()
            self.assertEqual(x.test(B()), 'B')
            self.assertEqual(x.test(D()), 'C')

    def test_overload_abstract_method(self):
        with registry_test_context():
            class TestBase(ABC):

                @abstractmethod
                def test(self, t: B) -> str:
                    ...

                @abstractmethod
                def test(self, t: C) -> str:
                    ...

            class Test(TestBase):

                @overload
                def test(self, t: B) -> str:
                    return 'B'

                @overload
                def test(self, t: C) -> str:
                    return 'C'


            x = Test()
            self.assertEqual(x.test(B()), 'B')
            self.assertEqual(x.test(C()), 'C')

    def test_overload_classmethod(self):
        with registry_test_context():

            class Test():

                @classmethod
                @overload
                def test(cls, t: B) -> str:
                    return 'B'

                @classmethod
                @overload
                def test(cls, t: C) -> str:
                    return 'C'


            x = Test()
            self.assertEqual(x.test(B()), 'B')
            self.assertEqual(x.test(C()), 'C')

    def test_overload_staticmethod(self):
        with registry_test_context():

            class Test():

                @staticmethod
                @overload
                def test(t: B) -> str:
                    return 'B'

                @staticmethod
                @overload
                def test(t: C) -> str:
                    return 'C'


            x = Test()
            self.assertEqual(x.test(B()), 'B')
            self.assertEqual(x.test(C()), 'C')

    def test_overload_variable_length(self):
        with registry_test_context():
            class Test():

                @overload
                def test(self, t: B) -> str:
                    return 'B'

                @overload
                def test(self, t: B, u: B) -> str:
                    return 'BB'


            x = Test()
            self.assertEqual(x.test(B()), 'B')
            self.assertEqual(x.test(B(), B()), 'BB')

    def test_overload_complicated(self):
        with registry_test_context():
            class Test():

                @overload
                def test(self, t: B) -> str:
                    return 'B'

                @overload
                def test(self, t: B, u: B) -> str:
                    return 'BB'

                @overload
                def test(self, t: B, u: C) -> str:
                    return 'BC'

                @overload
                def test(self, t: B, u: C, v: B) -> str:
                    return 'BCB'

                @overload
                def test(self, t: C, u: C) -> str:
                    return 'CC'

                @overload
                def test(self, t: B, u: C, v: B, w: B, o: List=[]) -> str:
                    return 'BCBBL'


            x = Test()
            self.assertEqual(x.test(B()), 'B')
            self.assertEqual(x.test(B(), B()), 'BB')
            self.assertEqual(x.test(B(), C()), 'BC')
            self.assertEqual(x.test(B(), C(), B()), 'BCB')
            self.assertEqual(x.test(C(), C()), 'CC')
            self.assertEqual(x.test(B(), C(), B(), B()), 'BCBBL')
            self.assertEqual(x.test(B(), C(), B(), B(), [1, 2, 3]), 'BCBBL')

    def test_overload_optional_ambiguous_variable_length(self):
        with self.assertRaises(TypeError) as context:
            with registry_test_context():
                class Test():

                    @overload
                    def test(self, t: B) -> str:
                        return 'B'

                    @overload
                    def test(self, t: B, o: List=[]) -> str:
                        return 'BL'


            self.assertTrue('Duplicate registration' in context.exception)

    def test_overload_optional_ambiguous(self):
        with self.assertRaises(TypeError) as context:
            with registry_test_context():
                class Test():

                    @overload
                    def test(self, t: B, o: Dict={}) -> str:
                        return 'BD'

                    @overload
                    def test(self, t: B, o: List=[]) -> str:
                        return 'BL'


            self.assertTrue('Duplicate registration' in context.exception)
