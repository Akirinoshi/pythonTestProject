from typing import Any


def get_not_nullable_attrs(obj: Any) -> dict[str, Any]:
    """
    Retrieves the attributes of an object that are neither None nor an empty string.

    :param obj: The object whose non-nullable attributes will be extracted.
        If the object is None, an empty dictionary is returned.
    :type obj: Any

    :return: A dictionary where keys are the names of attributes of 'obj' and
        values are the corresponding attribute values.
    :rtype: dict[str, Any]

    Example usage:

        class Example:
            def __init__(self):
                self.attr1 = None
                self.attr2 = "value"
                self.attr3 = ""

        example_instance = Example()
        non_nullable_attrs = get_not_nullable_attrs(example_instance)

        # non_nullable_attrs should be {'attr2': 'value'}
    """
    result = {}

    if obj is None:
        return result

    for k, v in obj.__dict__.items():
        if v is not None and v != "":
            result[k] = v

    return result
