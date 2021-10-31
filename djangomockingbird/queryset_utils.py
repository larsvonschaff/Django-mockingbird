#utility functions used for generating structures (dicts, lists, classes...) that are returned from methods of the querysets
from typing import Dict, Any, Iterable, List


def annotate_mock_class(kwargs: Dict[Any, Any], model_class: object) -> object:
    for arg in list(kwargs):
        val = kwargs[arg]
        setattr(model_class, str(arg), val)

    return model_class    


def make_mock_list_from_args(args: Iterable[Any]) -> List[int]:
    if len(list(args)) == 0:
        mock_values_list = [1]
    else:
        mock_values_list = [1 for x in range(len(list(args)))]

    return mock_values_list


def get_keys_from_dict(my_dict: Dict[Any, Any]) -> List[Any]:

    return [key for key in my_dict.keys()]


def make_mock_in_bulk_dict(*args: List[Any]) -> Dict[Any, Any]:
    mock_in_bulk_dict = {}

    if len(list(args)) == 0:
        mock_in_bulk_dict['1'] = ' '
    else:
        for item in args[0]:
            mock_in_bulk_dict[item] = ' '

    return mock_in_bulk_dict


def make_mock_aggregate_dict(kwargs: Dict[Any, Any]) -> Dict[str, Any]:
    mock_aggregate_dict = {}

    for arg in list(kwargs):
        val = kwargs[arg]
        mock_aggregate_dict[str(arg)] = val

    return mock_aggregate_dict


def annotate_return_value(return_value: Any, kwargs: Any) -> Any:
    if type(return_value) == dict:
        for arg in list(kwargs):
            return_value[str(arg)] = ' '

    return return_value

    
