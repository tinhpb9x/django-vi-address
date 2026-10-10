django-vi-address
=================

A Django app providing models, a REST API, and a data-import management
command for Vietnam's administrative divisions — provinces/cities and
wards.

Since July 1, 2025, Vietnam officially abolished the district (huyện)
administrative level nationwide (Resolution No. 1656/NQ-UBTVQH15 and
related merger resolutions). Starting with version 1.0.0, this package
reflects that change end-to-end: the hierarchy is now **province/city →
ward** (previously province/city → district → ward), and the bundled
dataset covers the post-merger 34 provinces/cities.

If you need the old three-level (province → district → ward) hierarchy,
pin to ``django-vi-address<1.0.0``.

Features
--------
- ``City`` and ``Ward`` models — ``Ward.parent_code`` points directly to
  its parent ``City``.
- Read-only REST API (Django REST Framework) to list cities and fetch a
  city with all of its wards.
- An ``insert_data`` management command that loads the bundled JSON
  dataset into your database. It upserts by ``code``, so re-running it
  after an upgrade updates rows in place and keeps their primary keys
  (and your foreign keys to them).
- ``City.note`` and ``Ward.note`` carry the resolution (nghị định) and
  merger/rename history, sourced from the official NSO catalogue
  (https://www.nso.gov.vn/phuong-phap-luan-thong-ke/danh-muc/don-vi-hanh-chinh/).

Requirements
------------
Python >= 3.6

Installation
------------
1. Create a new project::

    mkdir new_project && cd new_project

2. Create a virtual environment::

    virtualenv venv
    source venv/bin/activate

3. Install the package::

    pip install django-vi-address

Quick start
-----------

1. Add ``rest_framework`` and ``vi_address`` to ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        ...
        'rest_framework',  # new
        'vi_address',      # new
        ...
    ]

2. Include the ``vi_address`` URLconf in your project's ``urls.py``::

    # your_project/urls.py
    from django.urls import path, include

    urlpatterns = [
        ...
        path('api/address/', include('vi_address.urls')),
        ...
    ]

3. Run migrations::

    python manage.py migrate

4. Load (or, after upgrading, update) the data::

    python manage.py insert_data

   Options:

   - ``--prune``: also delete cities/wards no longer in the bundled data
     (cascades to rows referencing them).
   - ``--reset``: delete everything and re-insert (pre-1.1.0 behaviour;
     primary keys change and related rows are deleted).

API
---
- ``GET /api/address/cities`` — list all provinces/cities.
- ``GET /api/address/city/{city_id}`` — retrieve a city with its wards.

Running tests
-------------
::

    pip install django djangorestframework
    python runtests.py

Changelog
---------

1.1.0 (2026-10-10)
~~~~~~~~~~~~~~~~~~
Data refreshed from the official NSO catalogue (snapshot 2026-10-10).

**Added**

- ``City.note``: the resolution behind each province/city (also in the
  API).
- ``insert_data --prune`` and ``insert_data --reset``.
- Test suite (``python runtests.py``).

**Changed**

- Quảng Ninh (22), Bắc Ninh (24) and Đồng Nai (75) became
  centrally-governed cities (``type`` ``tinh`` → ``thanh-pho``,
  ``Thành phố …``); resolutions 36/2026/QH16, 39/2026/QH16,
  30/2026/QH16.
- 22 communes in Bắc Ninh and Đồng Nai became wards (``xa`` → ``phuong``);
  224 ward paths updated accordingly; 29 ward notes re-synced with NSO.
- ``insert_data`` now upserts by ``code`` in a transaction instead of
  deleting all rows first.
- ``City.code`` and ``Ward.code`` are unique (migration ``0002``).

**Fixed**

- Duplicated prefixes (``Xã Xã …``, ``Đặc khu Đặc khu …``), special-zone
  ``type`` ``"đặc khu"`` → ``dac-khu``, ``xã Bắc Sơn`` capitalisation,
  14 malformed slugs (``---``, apostrophes), and notes corrupted by a
  blanket "Phường Phường" replacement (e.g. "phường Phường Đúc").

**Upgrade notes**

1. ``python manage.py migrate vi_address`` (adds ``City.note`` and unique
   ``code``). If it reports duplicate codes, remove the duplicated rows
   (or delete all ``City`` rows) and migrate again.
2. ``python manage.py insert_data`` — rows are updated in place.
3. Review code relying on ``type == "đặc khu"`` (now ``"dac-khu"``),
   ``type`` of provinces 22/24/75 and of the 22 converted wards, or on
   the 14 changed slugs.

1.0.1 (2026-08-03)
~~~~~~~~~~~~~~~~~~~
**Breaking changes**

- Removed the ``District`` model and the district (huyện) administrative
  level entirely, reflecting Vietnam's official abolition of that level
  effective July 1, 2025 (Resolution No. 1656/NQ-UBTVQH15 and related
  merger resolutions).
- ``Ward.parent_code`` now references ``City`` directly instead of
  ``District``. The hierarchy is now ``City`` (province/city) → ``Ward``
  (ward).
- Removed the ``GET /api/address/district/{district_id}`` endpoint, and
  the now-unused ``DistrictSerializer``, ``DistrictDetailSerializer``,
  ``DistrictDetailAPIView`` and ``DistrictAdmin``.
- ``GET /api/address/city/{city_id}`` now returns ``wards`` nested
  directly instead of ``districts``.

**Added**

- ``Ward.note`` field capturing each ward's merger/rename history,
  sourced from the official resolution data.

**Changed**

- Refreshed the bundled address dataset (``vi_address/data/``) to match
  the post-merger 34 provinces/cities and their wards.

**Upgrade notes**

This is a breaking change. If you are upgrading from ``0.1.x``:

1. Run ``python manage.py makemigrations vi_address`` and
   ``python manage.py migrate`` — this drops the ``District`` table and
   alters ``Ward.parent_code`` to point to ``City``. Back up any custom
   data first.
2. Re-run ``python manage.py insert_data`` to reload the refreshed
   dataset.
3. Update any code referencing ``vi_address.models.District``,
   ``DistrictSerializer``, ``DistrictDetailAPIView``, or calling
   ``/api/address/district/{id}`` — these no longer exist.

0.1.6 and earlier
~~~~~~~~~~~~~~~~~~~
See git history.

License
-------
BSD-3-Clause