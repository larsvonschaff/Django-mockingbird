from django.db.models import ForeignKey, ManyToManyField, OneToOneField
import django
from django.db import models
from django.apps import apps
from .utils import make_spec_dict, get_custom_methods, create_function, set_backwards_managers, set_forwards_managers, get_model_manager
from . import queryset
import inspect
import types


def make_mocks(model_name, specs=None, model_method_specs=None):

    model_fields = model_name._meta.get_fields()

    # create dict to mimic model
    model_dict = make_spec_dict(model_fields, model_name, specs)

    # create class from the above dict
    mock_class = type(str(model_name), (object,), model_dict)

    if model_method_specs:
        for k, v in model_method_specs.items():
            # if the user attemps to define a nonexistant  custom method, raise error
            if k not in get_custom_methods(model_name):
                raise Exception(
                    "The model {} does not have a {} custom method".format(
                        model_name, k
                    )
                )
                # handling of custom model methods: user defines the model_method_specs dict, key is name of model, value is expected return
                # create function from these parameters and set it as an attribute of the mock
            func = create_function(k, mock_class, v)
            setattr(mock_class, str(k), func)

    manager_class = queryset.MockBaseQueryset(mock_class, model_dict)

    related_manager_class = queryset.MockRelatedManager(mock_class, model_dict)

    # the next two methods set manager classes to the mock which are meant to mimic this behaviour: https://docs.djangoproject.com/en/3.1/ref/models/relations/

    # set methods on the other side of foreign key and many-to-many relations
    set_backwards_managers(model_fields, mock_class, related_manager_class)

    # set methods on the forward side of a many-to-many relation
    set_forwards_managers(model_fields, mock_class, related_manager_class)

    manager_name = get_model_manager(model_name)

    def save(self):
        return mock_class()

    def delete():
        return (1, {str(mock_class.__name__): 1})

    def __str__(self):
        return str(mock_class.__name__)

    def __hash__(self):
        return 1

    def get_absolute_url(self):
        return "/fake_testing_url/{}".format(str(self.mock_class))

    def __init__(*args, **kwargs):
        pass

    # add model methods to mock
    setattr(mock_class, manager_name, manager_class)
    setattr(mock_class, "save", save)
    setattr(mock_class, "delete", delete)
    setattr(mock_class, "__init__", __init__)

    return mock_class
