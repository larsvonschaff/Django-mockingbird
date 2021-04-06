import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


setup(
    name="djangomockingbird",
    version="1.0.0",
    description="Easily write unit tests for Django without touching the database",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/larsvonschaff/Django-mockingbird",
    author_email="larsvonschaff@gmail.com",
    license="MIT",
    install_requires=["django"],
    packages=["djangomockingbird"],

)

