from distutils.core import setup
from setuptools import find_packages

setup(
    name='traffic-monitoring',
    packages=find_packages(where='src'),
    package_dir={'': 'src'}
)