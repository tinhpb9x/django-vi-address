import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from vi_address.models import City, Ward

DATA_DIR = Path(__file__).resolve().parent.parent.parent / 'data'

CITY_FIELDS = ('name', 'slug', 'type', 'name_with_type', 'note')
WARD_FIELDS = ('name', 'slug', 'type', 'name_with_type', 'path', 'path_with_type', 'note')


def load_json(path):
    try:
        with open(path, 'r', encoding='UTF-8') as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise CommandError(f'Cannot read {path}: {exc}')


class Command(BaseCommand):
    help = (
        'Insert or update cities and wards from the bundled data, matched by code. '
        'Existing rows keep their primary keys, so foreign keys pointing to them are preserved.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset', action='store_true',
            help='Delete all cities and wards before inserting (pre-1.1.0 behaviour; '
                 'cascades to rows referencing them).',
        )
        parser.add_argument(
            '--prune', action='store_true',
            help='Delete cities and wards that are no longer in the bundled data '
                 '(cascades to rows referencing them).',
        )

    def handle(self, *args, **options):
        cities_data = load_json(DATA_DIR / 'tinh_tp.json')
        wards_data = {}
        for city_code in cities_data:
            for ward_code, value in load_json(DATA_DIR / 'xa-phuong' / f'{city_code}.json').items():
                wards_data[int(ward_code)] = value

        with transaction.atomic():
            if options['reset']:
                Ward.objects.all().delete()
                City.objects.all().delete()
                self.stdout.write('Deleted all existing cities and wards (--reset).')

            cities = self.upsert_cities(cities_data)
            self.upsert_wards(wards_data, cities)
            self.handle_stale(
                set(int(code) for code in cities_data), set(wards_data), options['prune'],
            )
        self.stdout.write(self.style.SUCCESS('Done.'))

    def _upsert(self, model, fields, records):
        """records: {code: {field: value}} -> (created, updated) counts."""
        existing = model.objects.in_bulk(list(records), field_name='code')
        to_create, to_update = [], []
        for code, values in records.items():
            obj = existing.get(code)
            if obj is None:
                to_create.append(model(code=code, **values))
            elif any(getattr(obj, f) != v for f, v in values.items()):
                for f, v in values.items():
                    setattr(obj, f, v)
                to_update.append(obj)
        model.objects.bulk_create(to_create)
        if to_update:
            model.objects.bulk_update(to_update, list(fields))
        return len(to_create), len(to_update)

    def upsert_cities(self, cities_data):
        records = {
            int(code): {f: value.get(f, '') for f in CITY_FIELDS}
            for code, value in cities_data.items()
        }
        created, updated = self._upsert(City, CITY_FIELDS, records)
        self.stdout.write(f'Cities: {created} created, {updated} updated.')
        return City.objects.in_bulk(list(records), field_name='code')

    def upsert_wards(self, wards_data, cities):
        records = {}
        for code, value in wards_data.items():
            city = cities.get(int(value['parent_code']))
            if city is None:
                raise CommandError(f"Ward {code} references unknown city {value['parent_code']}")
            records[code] = {f: value.get(f, '') for f in WARD_FIELDS}
            records[code]['parent_code'] = city
        created, updated = self._upsert(Ward, WARD_FIELDS + ('parent_code',), records)
        self.stdout.write(f'Wards: {created} created, {updated} updated.')

    def handle_stale(self, city_codes, ward_codes, prune):
        stale_wards = Ward.objects.exclude(code__in=ward_codes)
        stale_cities = City.objects.exclude(code__in=city_codes)
        n_wards, n_cities = stale_wards.count(), stale_cities.count()
        if not (n_wards or n_cities):
            return
        if prune:
            stale_wards.delete()
            stale_cities.delete()
            self.stdout.write(f'Pruned {n_cities} cities and {n_wards} wards no longer in the data.')
        else:
            self.stdout.write(self.style.WARNING(
                f'{n_cities} cities and {n_wards} wards are no longer in the data; '
                'run with --prune to delete them.'
            ))
