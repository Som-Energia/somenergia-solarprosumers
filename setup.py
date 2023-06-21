#!/usr/bin/env python
from setuptools import setup, find_packages

from config import VERSION

readme = open("README.md").read()

setup(
    name="solarprosumers",
    version=VERSION,
    description="Web application to manage collective campaigns to purchase and install solar panels at home",
    author="Som Energia SCCL",
    author_email="info@somenergia.coop",
    url="https://github.com/som-energia/somenergia-solarprosumers",
    long_description=readme,
    license="GNU Affero General Public License v3 or later (AGPLv3+)",
    packages=find_packages(exclude=["*[tT]est*"]),
    scripts=[],
    install_requires=[
        "yamlns",
        "consolemsg",
        "mock",
        "b2btest",
        "nose",
        "rednose",
    ],
    include_package_data=True,
    test_suite="solarprosumers",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)
