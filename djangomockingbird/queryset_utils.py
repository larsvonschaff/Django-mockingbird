# utility functions used for generating structures (dicts, lists, classes...) that are returned from methods of the querysets


def annotate_mock_class(kwargs, model_class):
    for arg in list(kwargs):
        val = kwargs[arg]
        setattr(model_class, str(arg), val)

    return model_class


def make_mock_list_from_args(args):
    if len(list(args)) == 0:
        mock_values_list = [1]
    else:
        mock_values_list = [1 for x in range(len(list(args)))]

    return mock_values_list


def get_keys_from_dict(my_dict):

    return [key for key in my_dict.keys()]


def make_mock_in_bulk_dict(args):
    mock_in_bulk_dict = {}

    if len(list(args)) == 0:
        mock_in_bulk_dict["1"] = " "
    else:
        for item in args:
            mock_in_bulk_dict[item] = " "

    return mock_in_bulk_dict


def make_mock_aggregate_dict(kwargs):
    mock_aggregate_dict = {}

    for arg in list(kwargs):
        val = kwargs[arg]
        mock_aggregate_dict[str(arg)] = val

    return mock_aggregate_dict


def annotate_return_value(return_value, kwargs):
    if type(return_value) == dict:
        for arg in list(kwargs):
            return_value[str(arg)] = " "

    return return_value
