import inspect
import types

# construct a dict from the model
def make_spec_dict(
    model_fields,
    model_name,
    specs=None,
):
    fields = [field.name for field in model_fields if field.concrete]
    model_dict = {field: " " for field in fields}

    if specs:
        for k, v in specs.items():
            if k not in fields:
                # if the user has specified an invalid field, raise exception
                raise Exception(
                    "The model {} does not have a {} field".format(model_name, k)
                )

        model_dict.update(specs)

    model_dict["id"] = " "
    model_dict["pk"] = 1

    return model_dict


# get all methods of a model which are custom/user defined/not inherited.
def get_custom_methods(model_name):
    custom_methods = []
    for name, item in model_name.__dict__.items():
        if isinstance(item, types.FunctionType):
            custom_methods.append(name)

    return custom_methods


# function for creating functions with dynamic names and return values. used for mocking custom model methods.
def create_function(name, arg, return_value):
    def inner(arg):
        return return_value

    inner.__name__ = name
    return inner


# get name of model manager
def get_model_manager(model_name):
    manager_name = str(model_name._meta.default_manager)
    manager_name.split(".")

    return (manager_name.split("."))[2]


def set_backwards_managers(model_fields, mock_class, manager):

    # get all reverse relations
    reverse_relation_fields = [
        field
        for field in model_fields
        if field.auto_created and not field.concrete and not field.one_to_one
    ]

    for field in reverse_relation_fields:
        manager_name = (
            str(field.related_name) if field.related_name else str(field.name) + "_set"
        )
        if field.one_to_many or field.many_to_many:
            setattr(mock_class, manager_name, manager)

    return mock_class


def set_forwards_managers(model_fields, mock_class, manager):

    for field in model_fields:
        if field.many_to_many:
            setattr(mock_class, str(field), manager)

    return mock_class
