import json
import os
from django.core.management.base import BaseCommand, CommandError

try:
    from vi_address.models import City, Ward
except ImportError:
    raise CommandError("Please run 'python manage.py migrate' before and try again.")


from pathlib import Path
DATA_DIR = Path(__file__).resolve().parent.parent.parent


class Command(BaseCommand):
    help = 'Insert data cities, wards'

    def delete_old_data(self):
        City.objects.all().delete()
        Ward.objects.all().delete()

    def handle(self, *args, **kwargs):
        self.delete_old_data()
        self.insert_data_cities()
        self.insert_data_wards()
        print('done')

    def insert_data_cities(self):
        cities = City.objects.all()
        # if cities.count() > 0:
        #     raise CommandError("City model has a data.")
        # else:
        with open(os.path.join(DATA_DIR, 'data/tinh_tp.json'), 'r', encoding='UTF-8') as f:
            city_data = json.load(f)
            bulk_list = []
            for value in city_data.values():
                bulk_list.append(
                    City(
                        name=value['name'], slug=value['slug'], type=value['type'],
                        name_with_type=value['name_with_type'], code=int(value['code'])
                    )
                )
        City.objects.bulk_create(bulk_list)
        print('Insert data cities successfully!')

    def insert_data_wards(self):
        cities = City.objects.all()

        for city in cities:
            if city.code < 10:
                file_path = os.path.join(DATA_DIR, f'data/xa-phuong/0{city.code}.json')
            else:
                file_path = os.path.join(DATA_DIR, f'data/xa-phuong/{city.code}.json')
            with open(file_path, 'r', encoding='UTF-8') as f:
                try:
                    ward_data = json.load(f)
                    bulk_list = []
                    for value in ward_data.values():
                        bulk_list.append(
                            Ward(
                                name=value['name'], slug=value['slug'], type=value['type'],
                                name_with_type=value['name_with_type'],
                                path=value['path'], path_with_type=value['path_with_type'],
                                code=int(value['code']), note=value['note'],
                                parent_code=city
                            )
                        )
                    Ward.objects.bulk_create(bulk_list)
                except json.JSONDecodeError:
                    print(city.code, city.name_with_type)
                except TypeError:
                    print(city.code, city.name_with_type)
        print('Insert data wards successfully!')
