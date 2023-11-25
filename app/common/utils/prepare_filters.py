from typing import Any, Type, Optional

from sqlalchemy.sql.elements import SQLCoreOperations

from app import db

NUMERIC_TYPES = [int, float]


def get_value_limit_filter(
    model: Type[db.Model], param_name: str, param_value: Any
) -> Optional[SQLCoreOperations]:
    if param_name.startswith("min_") and type(param_value) in NUMERIC_TYPES:
        column_name = param_name[4:]
        column = getattr(model, column_name, None)

        if not column:
            return

        return column >= param_value  # type: ignore

    elif param_name.startswith("max_") and type(param_value) in NUMERIC_TYPES:
        column_name = param_name[4:]
        column = getattr(model, column_name, None)

        if not column:
            return

        return column <= param_value  # type: ignore


def prepare_filters(
    model: Type[db.Model], params: dict[str, Any]
) -> list[SQLCoreOperations]:
    """
    Prepare SQLAlchemy filter expressions based on provided parameters.

    Constructs a list of SQLAlchemy filter expressions based on the provided
    parameter mappings. It iterates through each item in the `params` dictionary
    and prepares appropriate filter expressions based on the parameter name
    and value. The function also uses `get_value_limit_filter` to create
    filtering conditions for parameters starting with "min_" and "max_" prefixes.

    :param model: The SQLAlchemy model on which the filtering is to be applied.
    :type model: Type[db.Model]
    :param params: A dictionary of parameter names and values to create filters.
        Parameter names should correspond to column names in the `model`. For
        limiting numeric columns, parameter names can start with "min_" or "max_".
        - For string values, the filter will be a case-insensitive LIKE condition.
        - For non-string values, the filter will check for equality.
        - For "min_" or "max_" parameters, special filtering will be applied.
    :type params: dict[str, Any]

    :return: A list of SQLAlchemy filter expressions based on provided parameters.
    :rtype: list[SQLCoreOperations]

    Example
    -------
    Given a model:

        class User(db.Model):
            name = db.Column(db.String)
            age = db.Column(db.Integer)

    And calling:

        filters = prepare_filters(User, {'name': 'Alice', 'min_age': 30})

    Will generate filters that can be used to retrieve users named 'Alice' and
    aged 30 or above from the SQLAlchemy query.
    """
    result = []

    for key, value in params.items():
        column = getattr(model, key, None)

        if not column:
            limit_filter = get_value_limit_filter(
                model=model, param_name=key, param_value=value
            )

            if limit_filter is not None:
                result.append(limit_filter)

            continue

        if type(value) is str:
            result.append(column.ilike(f"%{value}%"))
        else:
            result.append(column == value)

    return result
