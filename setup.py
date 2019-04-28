import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="programdom",
    version="1.0.0",
    url="https://github.com/vCra/mooshak2api",
    license='MIT',

    author="Aaron Walker",
    author_email="aaw13@aber.ac.uk",

    description="Learn how well your students know how to do code!",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests',)),


    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)