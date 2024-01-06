from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='vrchat_oscquery',
    version='0.1dev0',
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
