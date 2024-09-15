from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='vrchat_oscquery',
    version='1.0.0',
    author='snail', 
    author_email='vrchat_oscquery@snail.rocks',
    packages=find_packages(),
    install_requires=[
        "zeroconf",
        "python-osc",
        "aiohttp"
    ],
    long_description=open('README.md').read()
)
