import functools
import inspect
import typing
from typing import Type, Dict, Tuple, Callable


registry: Dict[str, Callable] = {}

def overload(func: Callable) -> Callable:
    """Decorator to allow overloading parameters of different types in python.

    Only use when overloading with the concrete type that will be expected as interfaces are not yet supported.
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
    # Convert to simple types...
    temp: Dict[str, Type] = {}
    for k, v in param_types.items():
        if isinstance(v, typing.Generic.__class__):
            v = v.__extra__  # type: ignore
        temp[k] = v
    # Order the types according to parameter list (excluding self)
    types: Tuple[Type, ...] = tuple([temp[k] for k in inspect.signature(func).parameters.keys() if k != 'self'])

    name: str = func.__name__
    ow = registry.get(name)
    if ow is None:
        # Create a decorated method since it doesn't exist already
        @functools.wraps(func)
        def wrapper(self: Callable, *args: Tuple) -> Callable:  # TODO generics/collections and interface support
            types: Tuple[Type, ...] = tuple(arg.__class__ for arg in args)

            # Find signature with matching parameter types
            func: Callable = wrapper.typemap.get(types)  # type: ignore
            if func is None:
                raise TypeError(f"'{name}' method has no matching signature for '{types}'")

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
