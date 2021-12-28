#!/usr/bin/env python
from pathlib import Path
from setuptools import find_packages, setup

setup(
    name="django-vi-address",
    version="0.1.4",
    description="A Django app to migrate Vietnam address.",
    long_description=Path("README.rst").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/tinhpb9x/django-vi-address",
    author="Tinh Pham Ba",
    author_email="tinhpb9x@gmail.com",
    license="BSD-3-Clause",  # Example license
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content"
    ],
    include_package_data=True,
    packages=find_packages(exclude=["tests", "tests.*", "licenses", "requirements"]),
    python_requires=">=3.6",
    install_requires=[
        "django",
        "djangorestframework==3.13.1"
    ]
)
