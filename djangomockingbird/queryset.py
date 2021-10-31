import collections
import datetime
from typing import Optional, Tuple, Callable, Union

from djangomockingbird.queryset_utils import *


#queryset that returns mock class objects
class MockBaseQueryset(object):

    CHAINABLE_METHODS = [
        'filter',
        'exclude',
        'prefetch_related',
        'order_by',
        'reverse',
        'distinct',
        'all',
        'union',
        'intersection',
        'difference',
        'select_related',
        'extra',
        'defer',
        'only',
        'using',
        'select_for_update',
        'raw',
    ]

    def __init__(self, mock_class: Callable, model_dict: Dict[Any, Any]):
        self.mock_class = mock_class
        self.model_dict = model_dict

    def __getattr__(self, name: str):
        if name in self.CHAINABLE_METHODS:
            return lambda *args, **kwargs: self
        else:
            raise AttributeError()

    def annotate(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> object:

        model_class = annotate_mock_class(kwargs, self.mock_class)

        return self      

    def values(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> object:
        return MockDerivedQueryset(self.model_dict)

    def values_list(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> object:

        mock_values_list = make_mock_list_from_args(args)
        mock_values_tuple = tuple(mock_values_list)
        mock_fields_list = get_keys_from_dict(self.model_dict)
        mock_named_tuple = collections.namedtuple('Mock_named_tuple', list(mock_fields_list))   # type: ignore

        if 'flat' in kwargs and kwargs['flat'] == True:
            return MockDerivedQueryset(mock_values_list)

        elif 'named' in kwargs and kwargs['named'] == True:

            return MockDerivedQueryset(mock_named_tuple) 
        else:
            return MockDerivedQueryset(mock_values_tuple)

    def dates(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> object:
        return MockDerivedQueryset(datetime.datetime(2000, 1, 1))

    def datetimes(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> object:
        return MockDerivedQueryset(datetime.datetime(2000, 1, 1))    

    def none(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> None:
        return None   

    #methods that do not return querysets
    def get(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> object:
        return self.mock_class()

    def create(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> None:
        return None

    def get_or_create(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> Tuple[object, bool]:
        return (self.mock_class(), True)

    def update_or_create(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> Tuple[object, bool]:
        return (self.mock_class(), True)

    def bulk_create(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> None:
        return None

    def bulk_update(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> None:
        return None

    def count(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> int:
        return 1

    def in_bulk(self, *args: List[Any], **kwargs: Optional[Dict[Any, Any]]) -> Dict[Any, str]:

        mock_in_bulk_dict = make_mock_in_bulk_dict(*args)
    
        return mock_in_bulk_dict

    def iterator(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> List[object]:
        return [self.mock_class()]    
    
    def latest(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> object:
        return self.mock_class() 
    
    def earliest(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> object:
        return self.mock_class()    

    def first(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> object:
        return self.mock_class()

    def last(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> object:
        return self.mock_class()         
    
    def aggregate(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> Dict[Any, Any]:

        mock_aggregate_dict = make_mock_aggregate_dict(kwargs)

        return mock_aggregate_dict

    def exists(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> bool:
        return True   

    def update(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> int:
        return 1    
    
    def delete(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> int:
        return 1

    def as_manager(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> object:
        return self
    #TODO

    def explain(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> str:
        return 'mock explain'

    #extra methods/protocols
    def __len__(self) -> int:
        return 1

    def __iter__(self) -> Iterable[object]:
        return iter([self.mock_class()])

    def __next__(self) -> object:
        return self.mock_class()

    def __getitem__(self, key: Any) -> object:
        return self.mock_class()

    #methods for evaluating querysets
    def repr(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> object:
        return self.mock_class()

    def list(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> List[object]:
        return [self.mock_class()]

    def bool(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> bool:
        return True


#queryset that returns something other than mock class objects: dicts, tuples, datetime objects etc.
class MockDerivedQueryset(MockBaseQueryset):

    def __init__(self, return_value: Union[Any, Dict[Any, Any]]):
        self.return_value = return_value
        if isinstance(self.return_value, dict):
            dict.__init__(self, return_value)   # type: ignore

    #methods that do not return querysets
    def get(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> Any:
        return self.return_value

    def get_or_create(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> Tuple[Any, bool]:
        return (self.return_value, True)

    def update_or_create(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> Tuple[Any, bool]:
        return (self.return_value, True)

    def iterator(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> List[Any]:
        return [self.return_value]    
    
    def latest(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> Any:
        return self.return_value
    
    def earliest(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> Any:
        return self.return_value

    def first(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> Any:
        return self.return_value

    def last(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> Any:
        return self.return_value

    #extra methods/protocols
    def __iter__(self) -> Iterable[Any]:
        return iter([self.return_value])

    def __next__(self) -> Any:
        return self.return_value

    def __getitem__(self, key: Any) -> Any:
        return self.return_value   

    #methods for evaluating querysets
    def repr(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> Any:
        return self.return_value

    def list(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> List[Any]:
        return [self.return_value]

    #other methods
    def annotate(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> object:

        annotated_return_value = annotate_return_value(self.return_value, kwargs)
       
        return MockDerivedQueryset(annotated_return_value)



class MockRelatedManager(MockBaseQueryset):
    def __init__(self, mock_class: Callable, model_dict: Dict[Any, Any]):
        self.mock_class = mock_class
        self.model_dict = model_dict

    def add(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> None:
        MockBaseQueryset(self.mock_class, self.model_dict)

    def create(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> None:
        MockBaseQueryset(self.mock_class, self.model_dict)

    def set(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> None:
        MockBaseQueryset(self.mock_class, self.model_dict)

    def remove(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> None:
        MockBaseQueryset(self.mock_class, self.model_dict)

    def clear(self, *args: Optional[List[Any]], **kwargs: Optional[Dict[Any, Any]]) -> None:
        MockBaseQueryset(self.mock_class, self.model_dict)

