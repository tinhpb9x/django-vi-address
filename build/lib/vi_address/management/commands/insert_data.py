import json
import os
from django.core.management.base import BaseCommand, CommandError

try:
    from vi_address.models import City, District, Ward
except ImportError:
    raise CommandError("Please run 'python manage.py migrate' before and try again.")


from pathlib import Path
DATA_DIR = Path(__file__).resolve().parent.parent.parent


class Command(BaseCommand):
    help = 'Insert data cities, districts, wards'

    # def add_arguments(self, parser):
    #     parser.add_argument('--datatype', type=str)

    def delete_old_data(self):
        City.objects.all().delete()
        District.objects.all().delete()
        Ward.objects.all().delete()

    def handle(self, *args, **kwargs):
        self.delete_old_data()
        self.insert_data_cities()
        self.insert_data_districts()
        self.insert_data_wards()
        # data_type = kwargs.get('datatype')
        # if data_type == 'city':
        #
        # elif data_type == 'district':
        #
        # elif data_type == 'ward':
        #
        # else:
        #     raise CommandError("'datatype' must be 'city', 'district' or 'ward'.")
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

    def insert_data_districts(self):
        # districts = District.objects.all()
        # if districts.count() > 0:
        #     raise CommandError("District model has a data.")
        #
        cities = City.objects.all()
        # if cities.count() == 0:
        #     raise CommandError("Please run 'python manage.py insert_data --datatype=city' before and try again.")

        for city in cities:
            if city.code < 10:
                file_path = os.path.join(DATA_DIR, f'data/quan-huyen/0{city.code}.json')
            else:
                file_path = os.path.join(DATA_DIR, f'data/quan-huyen/{city.code}.json')
            with open(file_path, 'r', encoding='UTF-8') as f:
                district_data = json.load(f)
                bulk_list = []
                for value in district_data.values():
                    bulk_list.append(
                        District(
                            name=value['name'], slug=value['slug'], type=value['type'],
                            name_with_type=value['name_with_type'],
                            path=value['path'], path_with_type=value['path_with_type'], code=int(value['code']),
                            parent_code=city
                        )
                    )
            District.objects.bulk_create(bulk_list)
        print('Insert data districts successfully!')

    def insert_data_wards(self):
        # wards = Ward.objects.all()
        # if wards.count() > 0:
        #     raise CommandError("Ward model has a data.")

        districts = District.objects.all()
        # if districts.count() == 0:
        #     raise CommandError("Please insert data of district model before and try again.")

        for district in districts:
            if district.code < 10:
                file_path = os.path.join(DATA_DIR, f'data/xa-phuong/00{district.code}.json')
            elif 10 <= district.code < 100:
                file_path = os.path.join(DATA_DIR, f'data/xa-phuong/0{district.code}.json')
            else:
                file_path = os.path.join(DATA_DIR, f'data/xa-phuong/{district.code}.json')
            with open(file_path, 'r', encoding='UTF-8') as f:
                try:
                    ward_data = json.load(f)
                    bulk_list = []
                    for value in ward_data.values():
                        bulk_list.append(
                            Ward(
                                name=value['name'], slug=value['slug'], type=value['type'],
                                name_with_type=value['name_with_type'],
                                path=value['path'], path_with_type=value['path_with_type'], code=int(value['code']),
                                parent_code=district
                            )
                        )
                    Ward.objects.bulk_create(bulk_list)
                except json.JSONDecodeError:
                    print(district.code, district.name_with_type)
                except TypeError:
                    print(district.code, district.name_with_type)
        print('Insert data wards successfully!')
