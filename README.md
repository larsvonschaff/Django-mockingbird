

# Django Mockingbird: the fastest way to write the fastest Django unit tests


![GitHub](https://img.shields.io/github/license/larsvonschaff/Django-mockingbird)
![PyPI](https://img.shields.io/pypi/v/djangomockingbird)




## 1. What is Django Mockingbird and why would I need it?

Until now, there were two options for writing tests for a Django application: either create objects in the database for every test or mock the database queries using [Unit test’s Mock](https://docs.python.org/3/library/unittest.mock.html). While the former is slow, the latter is complicated to write and read. Both add a lot of setup code to our tests. Django Mockingbird introduces a new way to write tests for Django, which is fast to run as well as simple to write.

## 2. How does it work?

It works by creating a mock object which behaves exactly like the Django model, but does not execute any queries under the hood. It only takes one line of code to use it in your test. It is not meant to be used in place of frameworks like [Pytest](https://docs.pytest.org/en/6.2.x/), but to complement them.

## 3. How do I use it?

### Installation 

```python
pip install djangomockingbird
```

### Usage

```python

from djangomockingbird import mock_model

@mock_model('myapp.myfile.MyModel')
def test_my_test():
    some_test_query = MyModel.objects.filter(bar='bar').filter.(foo='foo').first()
    #some more code
    #assertions here

```
With the mock_model decorator this test will pass no matter how complicated the query and will never touch the database.


### Specifiying mock return data

You can specify the values of specific fields of the model object you are mocking. If you don’t empty strings will be returned. Construct a dictionary with field names as keys and desired returs as values and pass it to the 'specs' argument of make_mocks. If you try to specify a nonexisant field as a key an error will be thrown, but you can specify any kind of value you want.

```python

@mock_model('myapp.myfile.MyModel', specs={'field': 'value'})

```

### Attention! Cases where returns must be specified: Model methods

If your model has custom methods and they are used by the test, you must specify their names and return data to the mock, otherwise your tests won't pass. 

```python

 model_method_specs = {'to_dict': {'': ''}}
@mock_model('myapp.myfile.MyModel', model_method_specs=model_method_specs)
 
 ```


## 4. Is it production ready? Can I help make it better? 

This is still a very new project, but is quite stable for the general use case. However, there are advanced use cases that are not yet supported, most notably [custom model managers](https://docs.djangoproject.com/en/3.1/topics/db/managers/#custom-managers). For those test cases you can try supplementing Django Mockingbird with your own code or other libraries. Because this tool is really just one elaborate mock model it is very flexible and plays well with pretty much anything.

We would appreciate you opening issues to bring any defects or oversights to light. Contributions are also kindly accepted - see more on the code arhitecture principles below if you are interested. 

## 5. Where can I read more details on the architecture?

Read about the how functional programming principles were used in the library [here](http://www.cmdctrlesc.xyz/post/6) and on metaprogramming features [here](http://www.cmdctrlesc.xyz/post/5).







