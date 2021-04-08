# Django Mockingbird: easily write unit tests for Django without touching the database

![PyPI](https://img.shields.io/pypi/v/djangomockingbird)
![GitHub](https://img.shields.io/github/license/larsvonschaff/Django-mockingbird)



## 1. What is Django Mockingbird?

Django Mockingbird is a utility library that helps you write unit tests for Django that do not touch the database. It does that by creating a mock object that mimics the behaviour of a specified Django model without actually executing any queries under the hood. The object automatically gets all the fields, methods and managers of the model, effectively providing a way to mock all of Django ORM’s behaviours with as little as one line of code per model. All you need to do is monkeypatch the actual Django model with Django mockingbird’s mock model for the duration of the test case.

## 2. What problem does it solve ?

Many developers believe that unit tests should not touch the database in any way. As soon as they do that falls under integration testing, however your app should ideally have both. Writing tests independant of the database also makes them much faster and more robust. Unfortunately writing tests this way is not in any way straightforward due to the [active record](https://en.wikipedia.org/wiki/Active_record_pattern) nature of the Django ORM. For simple use cases it might be enough to mock just one method on a model class, but for more complex queries with many chained filters, or for larger functions which require several models to be mocked for the test to pass this quickly becomes convoluted and even introduces false positives. Django Mockingbird is here to help with that.

## 3. How can I use it?

### Installation 

```python
pip install djangomockingbird
```

### Constructions the mocks

```python

from models import Model
from djangomockingbird import make_mocks

my_mock = make_mocks(Model)

```
my_mock is now an object that mimics Model's behaviour exactly.

### Using the mocks 


The most straightforward way is to monkeypatch the object directly using its absolute path. In this example function_to_test is a function that can containt any amount of queries involving Model. With Django mockingbird only the code below is necessary for this kind of test to pass, no matter how complicated the queries.


```python
from djangomockingbird import make_mocks
import myapp
import function_to_test

def test_my_test_case():

    myapp.myfile.Model = make_mocks(Model)
    result = function_to_test()
    #assertions here

```
A good way to use Django mockingbird is also with [Pytest's](https://docs.pytest.org/en/stable/) monkeypatch.


```python
import pytest
from djangomockingbird import make_mocks
import myapp
import function_to_test

def test_my_test_case(monkeypatch):
    mock_model = make_mocks(Model)
    monkeypatch.setattr('myapp.myfile.Model', mock_model)
    result = function_to_test()
    #assertions here

```

You can also use the mocks in many other ways, such as setting them as return values of functions (for example with unittests's mock.patch decorator), using only their specific class methods and of course combining them with other libraries and their features. Django Mockingbird is flexible, so be as creative as you like.

### Specifiying mock return data

You can specify the values of specific fields of the model object you are mocking. If you don’t empty strings will be returned. Construct a dictionary with field names as keys and desired returs as values and pass it to the 'specs' argument of make_mocks. If you try to specify a nonexisant field as a key an error will be thrown, but you can specify any kind of value you want.

```python

mock = make_mocks(Model, specs={'model_field':'desired_value'})

```


### Attention! Cases where returns must be specified: Model methods

If your model has custom methods and they are used by the test, you must specify their names and return data to the mock, otherwise your tests won't pass. 

```python

 model_method_specs = {'to_dict': {'': ''}}
 mock = make_mocks(Model, model_method_specs=model_method_specs)
 
 ```


## 5. Is it production ready? Can I help make it better? 

This is the very first version of Django Mockingbird. This is good to keep in mind in the sense of the possibility of bugs arising as well as in the sense of the core concept of the project being somewhat open to improvements.There are certainly advanced use cases that are not yet supported, most notably [custom model managers](https://docs.djangoproject.com/en/3.1/topics/db/managers/#custom-managers). For those test cases you can try supplementing Django Mockingbird with your own code or other libraries - because of its sole focus on the Django model object it plays well with pretty much everything. We would appreciate you opening issues to bring specific defects or oversights to light. Contributions are also kindly accepted - see more on the code arhitecture principles below if you are interested. 

## 6. Can you explain the rationale behind your architecture ? What should I know before contributing?

At its core, Django Mockingbird is a wrapper around the [Django meta API](https://docs.djangoproject.com/en/3.1/ref/models/meta/#). It uses it to inspect the model that is being mocked and then dynamically construct new classes based on those specifications as well as optionally the user’s specifications - ostensibly some basic metaprogramming is happening behind the scenes. The challenge was therefore mainly in avoiding unnecessary complexity in the API as well as in the code itself.

Most libraries in the Python ecosystem are written in an object-oriented style, despite there being a general appreciation in the community for Python’s functional features. The latter has arguably increased recently with more and more discussions arising on the benefits of abiding by functional programming principles despite not programming in a purely functional style or language, but this seems to have little effect on the conventions of Python library arhitecture. Attempting to challenge that with this project led to an interesting paradox: how do we use the best practices of functional programming in a library that deals with something as inherently object-oriented as Django’s object-relational mapper? Django Mockingbird implements this by keeping functions (computations) and classes (state) as separate as possible. The functions are pure and the classes are as devoid of logic as possible. Classes are kept in queryset.py, logic is kept in utils.py and they both come together in make_mocks.py, to form mock objects  with the appropriate behaviour. The main function make_mocks is also a pure and deterministic function,  always returning the same object with the same inputs. Another upside of doing it this way is that unit tests only need to be written for the functions where the logic lives, which are also pure, which makes tests basically just assertions.

All of this is good to keep in mind when contributing to this project.





