# Django Mockingbird: the fastest way to write the fastest Django unit tests

![PyPI](https://img.shields.io/pypi/v/djangomockingbird)
![GitHub](https://img.shields.io/github/license/larsvonschaff/Django-mockingbird)



## 1. What is Django-mockingbird and why would I need it?

Until now, there were two options for writing tests for a Django application: either create objects in the database for every test or mock the database queries using [Unit test’s Mock](https://docs.python.org/3/library/unittest.mock.html). While the former is slow, the latter is complicated to write and read. Both add a lot of setup code to our tests. Django-mockingbird introduces a new way to write tests for Django, which is fast to run as well as simple to write.

## 2. How does it work?

It works by creating a mock object which behaves exactly like the Django model in your test, but does not execute any queries under the hood. It only takes one line of code to use it in your test. It is not meant to be used in place of frameworks like Pytest, but to complement them.

## 3. How do I use it?

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


## 4. Is it production ready? Can I help make it better? 

For the general case it is but there are certainly advanced use cases that are not yet supported, most notably [custom model managers](https://docs.djangoproject.com/en/3.1/topics/db/managers/#custom-managers). For those test cases you can try supplementing Django Mockingbird with your own code or other libraries. Because this tool is really just one elaborate mock Model it is very flexible and plays well with pretty much anything. We would appreciate you opening issues to bring specific defects or oversights to light. Contributions are also kindly accepted - see more on the code arhitecture principles below if you are interested. 

## 5. Where can I read more details on the architcture and stuff?

Read about the use of functional programming principles in the library [here](http://www.cmdctrlesc.xyz/post/6) and on the use of Python's metaprogramming features [here](http://www.cmdctrlesc.xyz/post/5)







