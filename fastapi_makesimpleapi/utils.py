"""Simple api generator."""

import inspect
from typing import Any, Callable

from fastapi import APIRouter, Depends, Query


def get_typed_params(call: Callable[..., Any]) -> list[inspect.Parameter]:
    """Get typed parameters from a function except self."""
    signature = inspect.signature(call)

    typed_params = []
    for param in signature.parameters.values():
        if param.name == "self":
            continue

        if str(param.annotation).startswith("list"):
            param = param.replace(default=Query([]))

        typed_params.append(param)
    return typed_params


def snake_to_pascal(snake_case: str) -> str:
    """Convert snake case to pascal case."""
    return "".join(word.capitalize() for word in snake_case.split("_"))


def make_simple_api(
    router: APIRouter,
    http_method: str,
    url: str,
    klass: object,
    method_name: str,
) -> None:
    """Make just-call-service api from service method."""
    SERVICE_ARGUMENT_NAME = "service"

    method = getattr(klass, method_name)

    params = get_typed_params(method)
    params.append(
        inspect.Parameter(
            name=SERVICE_ARGUMENT_NAME,
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default=Depends(),
            annotation=klass,
        ),
    )
    params = inspect.Signature(params)
    return_type = inspect.signature(method).return_annotation

    async def simple_api(*args, **kwargs):
        bound_arguments = params.bind(*args, **kwargs)
        bound_arguments.apply_defaults()
        method = getattr(kwargs[SERVICE_ARGUMENT_NAME], method_name)
        kwargs.pop(SERVICE_ARGUMENT_NAME)
        return method(*args, **kwargs)

    simple_api.__signature__ = params
    simple_api.__annotations__ = {"return": return_type}
    simple_api.__name__ = method_name

    router_decorator = getattr(router, http_method)
    router_decorator(url, response_model=return_type)(simple_api)
