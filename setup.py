from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='imagechain',
    packages=['imagechain'],
    version='0.1',
    license='MIT',
    install_requires=[],
    author='p-geon',
    author_email='alchemic4s@gmail.com',
    url='https://github.com/p-geon/imagechain',
    description='Image plotting & Image conversion',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='image plot',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ], 
)