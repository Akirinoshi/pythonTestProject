import types
from typing import Callable, Tuple, Any

from pydantic import parse_obj_as, ValidationError

BUILTIN_TYPES = vars(types).values()


def is_builtin_type(type_: Any) -> bool:
    return type(type_) in BUILTIN_TYPES


def validate_path_params(func: Callable, kwargs: dict) -> Tuple[dict, list]:
    """
    Function aimed to patch flask_pydantic.core.validate_path_params.
    The difference is that this function skips any function params that have non-builtin type.
    This is needed to avoid problems with injected params, for which pydantic_validate raises
    error like RuntimeError: no validator found for <class '...'>, see arbitrary_types_allowed in Config
    """
    errors = []
    validated = {}
    for name, type_ in func.__annotations__.items():
        if name in {"query", "body", "form", "return"} or not is_builtin_type(type_):
            continue
        try:
            value = parse_obj_as(type_, kwargs.get(name))
            validated[name] = value
        except ValidationError as e:
            err = e.errors()[0]
            err["loc"] = [name]
            errors.append(err)
    kwargs = {**kwargs, **validated}
    return kwargs, errors
