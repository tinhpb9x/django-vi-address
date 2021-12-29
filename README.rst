=====
django-vi-address
=====
This is a Django project about provinces/cities, districts, wards of Vietnam. The project provides a model to store data about provinces/cities, districts and wards of Vietnam.

Requirements
-----------
Python >= 3.6

Installation
-----------
1. Create a new project
::
    mkdir new_project && cd new_project
2. Create a new virtual environment for this project
::
    virtualenv venv
    source venv/bin/activate
3. Install using `pip`
::

    (venv) $ pip install django-vi-address


Quick start
-----------

1. Add "rest_framework", "vi_address" to your INSTALLED_APPS setting like this::
::

    INSTALLED_APPS = [

        ...
        'rest_framework',
        'vi_address',
        ...

    ]


2. Include the "vi_address" URLconf in your project urls.py like this::
::

    path('api/addresss/', include('vi_address.urls')),

3. Create the models.
::
    python manage.py migrate

4. Insert data cities of Vietnam.
::
    python manage.py insert_data --datatype=city

5. Insert data districts of Vietnam.
::
    python manage.py insert_data --datatype=district

6. Insert data wards of Vietnam.
::
    python manage.py insert_data --datatype=ward

Endpoint
========
1. Get cities list
::
    /api/address/cities
2. Get districts list of a city
::
    /api/address/city/{city_id}
3. Get wards list of a district
::
    /api/address/district/{district_id}