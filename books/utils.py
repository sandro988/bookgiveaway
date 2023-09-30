from typing import Dict, Any, List, Union
from django.db.models import Model


def transform_genres_and_authors(
    data: Dict[str, Any],
    model_field: str,
    model_class: Model,
) -> Dict[str, Any]:
    """
    Transforms genre or author field in the input data to corresponding
    model objects either Genre or Author. Also capitalizes genre names and
    title-cases author names if necessary to ensure that no duplicate
    objects are created.

    Parameters:
        data (dict): The input data to be transformed.
        model_field (str): The name of the field to transform for example "genre" or "author".
        model_class (Genre or Author): The model class to create objects for.

    Returns:
        dict: The transformed data with the field converted to a list of model objects.
    """
    field_names = data.get(model_field)
    if field_names:
        field_objects = []
        for field_name in field_names:
            field_name = (
                field_name.capitalize()
                if model_field == "genre"
                else field_name.title()
            )
            field_kwargs = {f"{model_field}_name": field_name}
            field_object, _ = model_class.objects.get_or_create(**field_kwargs)
            field_objects.append(field_object)
        data[field_name] = field_objects
    return data
