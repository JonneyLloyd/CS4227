import functools
import inspect
import typing
from typing import Type, Optional, Dict, Tuple, Callable, Generator
from contextlib import contextmanager


def _strip_self(args: Tuple) -> Tuple:
    """
    Filter out 'self' and 'cls' from the beggining of the supplied args.
    """
    return args if args[0] != 'self' and args[0] != 'cls' else args[1:]


def _get_args(func: Callable) -> Tuple:
    """
    Get the required arguments, including default
    """
    args, *_ = inspect.getfullargspec(func)
    return tuple(args)


def _get_required_args(func: Callable) -> Tuple:
    """
    Get the required, non default arguments
    """
    args, varargs, varkw, defaults, *_ = inspect.getfullargspec(func)
    if defaults:
        args = args[:-len(defaults)]
    return tuple(args)


def _params_match_signature(func: Callable, func_types: Tuple[Type, ...], param_types: Tuple[Type, ...]) -> bool:
    """
    Determine if func with non optional parameters func_types can be parameterised with param_types.
    """
    # Lengths don't match
    if not (len(_strip_self(_get_required_args(func))) <= len(param_types) <= len(_strip_self(_get_args(func)))):
        return False

    # Types match
    return all(issubclass(p, t) for t, p in zip(func_types, param_types))


registry: Dict[str, Callable] = {}


@contextmanager
def registry_test_context() -> Generator:
    """A context manager for resetting between unit tests"""
    global registry
    registry = {}

    yield

    registry = {}


def overload(func: Callable) -> Callable:
    """Decorator to allow overloading parameters of different types in python.

    Be careful with this as python duck typing us awkward and this may not account for everything.

    Useful for the visitor pattern.

    Motivations:
        Take this inheritance hierarchy as an example:

            class A():
                ...


            class B(A):
                ...


            class C(A):
                ...

        We want to be able to accept both B and C as parameters, but with a different implementation i.e. overloading.
        One one first try this:

            class Test():

                def test(self, t: B) -> None:
                    print('B')

                def test(self, t: C) -> None:
                    print('C')

        Although it compiles, python just ignores the first implementation completely.
        A work arround is provided when using type annotations and stubs:

            class Test():

                def test(self, t: B) -> None:
                    ...

                def test(self, t: C) -> None:
                    ...

                def test(self, t):
                    if isinstance(t, B):
                        print('B')
                    if isinstance(t, C):
                        print('C')

        This solution just bloats the class as the stubs aren't really needed since type checking occurs.
        This decorator fixes this problem through introspection and type annotations:

            class Test():

                @overload
                def test(self, t: B) -> None:
                    print('B')

                @overload
                def test(self, t: C) -> None:
                    print('C')


            >>> x = Test()
            >>> x.test(B())
            'B'
            >>> x.test(C())
            'C'

    """
    if not hasattr(func, '__annotations__'):
        raise TypeError("Not type annotations found {}".format(func))

    param_types: Dict[str, type] = {k: v for k, v in func.__annotations__.items() if k != 'return'}
    args = _get_required_args(func)
    static = not ('self' in args or 'cls' in args)
    types: Tuple[Type, ...] = tuple([param_types[k] for k in _strip_self(args)])

    name: str = func.__module__ + "." + func.__name__
    ow = registry.get(name)
    if ow is None:
        # Create a decorated method since it doesn't exist already
        @functools.wraps(func)
        def wrapper(self: Callable, *args: Tuple) -> Callable:  # TODO generics/collections and function support
            if static:
                args = tuple([self, *args])
                self = None
            types: Tuple[Type, ...] = tuple(arg.__class__ for arg in args)

            # Find signature with matching parameter types
            func: Optional[Callable] = None
            for k, v in wrapper.typemap.items():
                if _params_match_signature(v, k, types):
                    func = v
            if func is None:
                raise TypeError(f"'{name}' method has no matching signature for '{types}'")

            if static:
                return func(*args)
            return func(self, *args)  # Call the matching method

        # wrapper contains a type map for each of the signatures for a single method name
        wrapper.typemap = {}  # type: ignore
        # Add the wrapper to the registry for later, also get ready to return it
        ow = registry[name] = wrapper

    if types in ow.typemap:  # type: ignore
        raise TypeError(f"Duplicate registration, the '{name}' method already has a signature for '{types}'")

    # Map the parameter list types to the correct implementation for the given method name
    ow.typemap[types] = func  # type: ignore

    # Return a new method capable of dispatching to the correct signatures
    return ow
