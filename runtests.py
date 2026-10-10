#!/usr/bin/env python
"""Run the vi_address test suite without a host project: ``python runtests.py [test labels]``."""
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

settings.configure(
    DEBUG=False,
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'rest_framework',
        'vi_address',
    ],
    ROOT_URLCONF='vi_address.urls',
    DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
    USE_TZ=True,
)


def main():
    django.setup()
    runner = get_runner(settings)(verbosity=2)
    failures = runner.run_tests(sys.argv[1:] or ['vi_address'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    main()
