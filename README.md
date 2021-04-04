# Django-mockingbird: easily write unit tests for Django without touching the database



## 1. What is Django-mockingbird?

Django-mockingbird is a utility library that helps you write unit tests for Django that do not touch the database. It does that by creating a mock object that mimics the behaviour of a specified Django model without actually executing any queries under the hood. The object automatically gets all the fields, methods and managers of the model, effectively providing a way to mock all of Django ORM’s behaviours with as little as one line of code per model. All you need to do is monkeypatch the actual Django model with Django-mockingbird’s mock model for the duration of the test case, either manually or with the use of other libraries.

## 2. What problem does it solve ?

Many developers believe that unit tests should not touch the database in any way. As soon as they do they fall under integration testing, however your app should ideally have both. But writing unit tests this way is not in any way straightforward due to the active record nature of the Django ORM. For simple use cases it might be enough to mock just one method on a model class, but for more complex queries with many chained filters, or for larger functions which require several models to be mocked for the test to pass this quickly becomes completely convoluted and even undermines the very point of unit tests by introducing false positives.

## 3. How can I use it?


### Constructions the mocks

```python

from models import Model
from django-mockingbird import make_mocks

my_mock = make_mocks(Model)

```
my_mock is now an object that mimics Model.

### Using the mocks 

Monkeypatching the object directly using its absolute path:

```python
from django-mockingbird import make_mocks
import myapp

def test_my_test_case():

    myapp.myfile.myfunction.Model = make_mocks(Model)

```

Monkeypatching the object using unittest's mock.patch decorator:

```python
from django-mockingbird import make_mocks
from unittest.mock import patch

@patch(myapp.myfile.myfunction.Model)
def test_my_test_case(mock_model):
    mock_model = make_mocks(Model)


```

### Specifiying return data

You can specify the values of specific fields of the model object you are mocking. If you don’t empty strings will be returned. Construct a dictionary with keys for field names and values for a desired return value and pass it to the 'specs' argument of make_mocks. If you try to specify a nonexisant field an error will be thrown.

```python

mock = make_mocks(Model, specs={‘model_field’:’desired_value’})

```




#### Attention! Cases where returns must be specified:

If your model has custom methods, you must specify their names and their return to the mock. You will likely need to specify the same data type your actual method returns to make your tests pass.

```python

 model_method_specs = {'to_dict': {'': ''}}
 mock = make_mocks(Event, model_method_specs=model_method_specs)
 
 ```





## 5. Is it production ready? Can I help make it better? 

This is the very first version of Django-mockingbird. This is good to keep in mind in the sense of the possibility of bugs arising as well as in the sense of the core concept of the project being somewhat open to improvements.There are certainly advanced use cases that are not yet supported, most notably custom model managers. For those test cases you can try supplementing Django-mockingbird with your own code or other libraries - because of its sole focus on the Django model object it plays well with pretty much everything. We would appreciate you opening issues to bring specific defects or oversights to light. Contributions are also kindly accepted - see more on the code arhitecture principles below if you are interested. 

## 6. Can you explain the rationale behind your architecture ? What should I know before contributing?

At its core, Django-mockingbird is a wrapper around the Django meta API. It uses it to inspect the model that is being mocked and then dynamically construct new classes based on those specifications as well as optionally the user’s specifications - ostensibly some basic metaprogramming is happening behind the scenes. The challenge was therefore mainly in avoiding unnecessary complexity in the API as well as in the code itself.

Looking through the Python ecosystem, most libraries are written in a completely object-oriented style, despite there being a general appreciation in the community for Python’s functional features. The latter has arguably increased recently with more and more discussions arising on the benefits of abiding by functional programming principles despite not programming in a purely functional style or language, but this seemed to have little effect on the conventions of Python library arhitecture. Attempting to challenge that with this project led to an interesting paradox: how do we use the best practices of functional programming in a library that deals with something as inherently object-oriented as Django’s object-relational mapper? Django-mockingbird’s implements this by keeping functions (computations) and classes (state) as separate as possible. The functions are pure and the classes are as devoid of logic as possible. Classes are kept in  queryset.py, logic is kept in utils.py and they both come together in make_mocks.py, to form mock objects  with the appropriate behaviour. The main function make_mocks is also a pure and deterministic function,  always returning the same object with the same inputs. Another upside of doing it this way is that unit tests only need to be written for the functions where the logic lives, which are also pure, which makes tests basically just assertions.

All of this is good to keep in mind when contributing to this project.





