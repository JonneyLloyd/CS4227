from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic, Optional, Tuple, Dict, Any
import logging


logger = logging.getLogger(__name__)


class GenericABC(ABC):

    def _get_generic_type(self, gen_type: TypeVar) -> Type:
        """Find the parameterized class of a given TypeVar so that it can be used for something useful.

            Using introspection, a depth first search finds the generic type placeholder starting with
            the subclass up to the superclass where the type placeholder is needed.
            Once it is found, it's index (if other generics are present) is propagated until a parameterized
            type is found. This type is returned.

            Parameters
            ----------
            gen_type (TypeVar)
                The generic type placeholder to find an implementation for.

            Returns
            -------
            Type
                The parameterized type.


            Example of a class traversal (some attributes ommited):
                (Pdb) vars(c.__class__)
                mappingproxy({
                '__module__': 'modules.demo.demo_interceptor',
                '__origin__': None,
                '__parameters__': (),
                '__args__': None,
                '__orig_bases__': (framework.interceptor.source_interceptor.SourceInterceptor[modules.demo.demo_config.DemoConfig],),
                })

                (Pdb) vars(c.__class__.__orig_bases__[0])
                mappingproxy({
                '__module__': 'framework.interceptor.source_interceptor',
                '__origin__': framework.interceptor.source_interceptor.SourceInterceptor,
                '__parameters__': (),
                '__args__': (<class 'modules.demo.demo_config.DemoConfig'>,),
                '__orig_bases__': (framework.interceptor.configurable_interceptor.ConfigurableInterceptor[~S], typing.Generic[~S])
                })

                (Pdb) vars(c.__class__.__orig_bases__[0].__orig_bases__[0])
                mappingproxy({
                '__module__': 'framework.interceptor.configurable_interceptor',
                '__origin__': framework.interceptor.configurable_interceptor.ConfigurableInterceptor,
                '__parameters__': (~S,),
                '__args__': (~S,),
                '__orig_bases__': (<class 'abc.ABC'>, typing.Generic[~T])
                })

                (Pdb) vars(c.__class__.__orig_bases__[0].__orig_bases__[0].__orig_bases__[1])
                mappingproxy({
                  '__module__': 'typing',
                  '__origin__': typing.Generic,
                  '__parameters__': (~T,),
                  '__args__': (~T,),
                  '__orig_bases__': ()})

        """
        logger.info(f'Starting search for generic type {gen_type} in class {self.__class__}')
        # Start the recursive search.
        # Directly parameterized classes use self.__orig_class__.
        # Classes with no direct generics but with generic parameters in a hierarchy use self.__class__
        clazz, _ = self.__find_type_var(self.__orig_class__ if hasattr(self, '__orig_class__') else self.__class__, gen_type)
        return clazz

    def __find_type_var(self, clazz: Type, gen_type: TypeVar, i: int=0) -> Tuple[Optional[Type], Optional[int]]:
        # Not a Generic type
        if not hasattr(clazz, '__parameters__'):
            return None, None

        space = "  " * i
        logger.info(f'{space}Searching for generic type {gen_type} in class {clazz.__name__}')
        # Check if this class contains the generic type
        if gen_type in clazz.__parameters__:
            logger.info(f'{space}--> Found generic type {gen_type} in class {clazz.__name__}')
            return None, clazz.__parameters__.index(gen_type)

        # Keep searching base classes
        for base in clazz.__orig_bases__:
            # Recursively until the generic type is found
            typ, pos = self.__find_type_var(base, gen_type, i+1)
            if pos is not None:
                # Generic found
                if isinstance(clazz.__args__[pos], TypeVar):
                    # Still only a TypeVar, keep going
                    return None, pos
                else:
                    # Not a TypeVar, therefore must be the parameterized type, propagate up
                    logger.info(f'{space}Found {clazz.__args__[pos]}')
                    return clazz.__args__[pos], None
            if typ is not None:
                # Actual parameterized generic type found, keep propagating
                return typ, None

        return None, None  # Failure
