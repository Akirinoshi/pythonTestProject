from typing import Type

from pydantic import BaseModel, create_model


def create_filter_model_with_limits(model_class: Type[BaseModel]) -> Type[BaseModel]:
    """
    Create a new Pydantic model for filtering purposes, based on another model,
    by extending its fields with optional minimum and maximum limit fields for
    numeric types.

    This function dynamically creates a new Pydantic model that can be used
    for filtering instances of the input model. It inspects each field of the
    input model. If the field is of type `int` or `float`, two new fields will
    be added to the filter model: `min_<field_name>` and `max_<field_name>`,
    which can be used to specify minimum and maximum allowable values for that
    field, respectively. For non-numeric field types, the original field will
    be included as-is.

    :param model_class: The Pydantic model based on which the filter model is to be created.
    :type model_class: Type[BaseModel]

    :return: A new Pydantic model class with optional min/max fields for numeric types.
    :rtype: Type[BaseModel]

    Example usage:
    -----

    Given a model:

        class Person(BaseModel):
            name: str
            age: int

    The function will generate a new model similar to:

        class PersonFilter(BaseModel):
            name: Optional[str] = None
            age: Optional[str] = None
            min_age: Optional[int] = None
            max_age: Optional[int] = None
    """

    fields = {}

    for field_name, field in model_class.__fields__.items():
        if field.type_ in (int, float):
            fields[f"min_{field_name}"] = (field.type_, None)
            fields[f"max_{field_name}"] = (field.type_, None)
        fields[field_name] = (field.type_, None)

    return create_model(model_class.__name__, **fields)
