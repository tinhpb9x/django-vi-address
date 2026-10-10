import json
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from .management.commands.insert_data import DATA_DIR
from .models import City, Ward

N_CITIES = 34
N_WARDS = 3321
VALID_CITY_TYPES = {'tinh', 'thanh-pho'}
VALID_WARD_TYPES = {'phuong', 'xa', 'dac-khu'}
PREFIX_DUPES = ('Phường Phường', 'Xã Xã', 'Tỉnh Tỉnh', 'Đặc khu Đặc khu', 'Tỉnh Thành phố')


def insert_data(*args):
    out = StringIO()
    call_command('insert_data', *args, stdout=out)
    return out.getvalue()


class BundledDataTests(TestCase):
    """Sanity checks on vi_address/data, independent of the database."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with open(DATA_DIR / 'tinh_tp.json', encoding='UTF-8') as f:
            cls.cities = json.load(f)
        cls.wards = {}
        for city_code in cls.cities:
            with open(DATA_DIR / 'xa-phuong' / f'{city_code}.json', encoding='UTF-8') as f:
                cls.wards.update(json.load(f))

    def test_counts_and_types(self):
        self.assertEqual(len(self.cities), N_CITIES)
        self.assertEqual(len(self.wards), N_WARDS)
        self.assertEqual({c['type'] for c in self.cities.values()}, VALID_CITY_TYPES)
        self.assertEqual({w['type'] for w in self.wards.values()}, VALID_WARD_TYPES)

    def test_no_duplicated_unit_prefixes(self):
        for ward in self.wards.values():
            for key in ('name', 'name_with_type', 'path', 'path_with_type'):
                with self.subTest(code=ward['code'], field=key):
                    self.assertFalse(any(d in ward[key] for d in PREFIX_DUPES), ward[key])

    def test_wards_reference_their_file_city(self):
        for ward in self.wards.values():
            self.assertIn(ward['parent_code'], self.cities)
            city = self.cities[ward['parent_code']]
            self.assertTrue(ward['path_with_type'].endswith(', ' + city['name_with_type']))


class InsertDataTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        insert_data()

    def test_loads_everything(self):
        self.assertEqual(City.objects.count(), N_CITIES)
        self.assertEqual(Ward.objects.count(), N_WARDS)
        quang_ninh = City.objects.get(code=22)
        self.assertEqual(quang_ninh.name_with_type, 'Thành phố Quảng Ninh')
        self.assertIn('36/2026/QH16', quang_ninh.note)
        self.assertEqual(Ward.objects.get(code=7294).name_with_type, 'Phường Bố Hạ')

    def test_rerun_is_idempotent_and_keeps_ids(self):
        ids = dict(Ward.objects.values_list('code', 'id'))
        output = insert_data()
        self.assertIn('Cities: 0 created, 0 updated.', output)
        self.assertIn('Wards: 0 created, 0 updated.', output)
        self.assertEqual(dict(Ward.objects.values_list('code', 'id')), ids)

    def test_rerun_restores_changed_rows_in_place(self):
        ward = Ward.objects.get(code=7294)
        other_city = City.objects.get(code=1)
        Ward.objects.filter(pk=ward.pk).update(name='Xã Bố Hạ', type='xa', parent_code=other_city)
        City.objects.filter(code=22).update(type='tinh', note='')

        output = insert_data()

        self.assertIn('Cities: 0 created, 1 updated.', output)
        self.assertIn('Wards: 0 created, 1 updated.', output)
        ward.refresh_from_db()
        self.assertEqual((ward.name, ward.type, ward.parent_code.code), ('Phường Bố Hạ', 'phuong', 24))
        self.assertEqual(City.objects.get(code=22).type, 'thanh-pho')

    def test_missing_rows_are_created(self):
        Ward.objects.filter(code=7294).delete()
        self.assertIn('Wards: 1 created, 0 updated.', insert_data())
        self.assertTrue(Ward.objects.filter(code=7294).exists())

    def _add_stale_rows(self):
        city = City.objects.create(code=99, name='Cũ', slug='cu', type='tinh', name_with_type='Tỉnh Cũ')
        Ward.objects.create(code=99999, name='Xã Cũ', slug='xa-cu', type='xa', name_with_type='Xã Cũ',
                            path='', path_with_type='', note='', parent_code=city)

    def test_stale_rows_are_kept_without_prune(self):
        self._add_stale_rows()
        output = insert_data()
        self.assertIn('1 cities and 1 wards are no longer in the data', output)
        self.assertTrue(Ward.objects.filter(code=99999).exists())

    def test_prune_deletes_stale_rows(self):
        self._add_stale_rows()
        output = insert_data('--prune')
        self.assertIn('Pruned 1 cities and 1 wards', output)
        self.assertFalse(City.objects.filter(code=99).exists())
        self.assertFalse(Ward.objects.filter(code=99999).exists())
        self.assertEqual(Ward.objects.count(), N_WARDS)

    def test_reset_recreates_rows(self):
        old_id = Ward.objects.get(code=7294).id
        insert_data('--reset')
        self.assertEqual(Ward.objects.count(), N_WARDS)
        self.assertNotEqual(Ward.objects.get(code=7294).id, old_id)


class ApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        insert_data()

    def test_city_list(self):
        response = self.client.get('/cities')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), N_CITIES)
        self.assertIn('note', data[0])

    def test_city_detail_includes_note_and_wards(self):
        city = City.objects.get(code=24)
        response = self.client.get(f'/city/{city.pk}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name_with_type'], 'Thành phố Bắc Ninh')
        self.assertIn('39/2026/QH16', data['note'])
        self.assertEqual(len(data['wards']), city.wards.count())
