=====
Provinces of Vietnam using Django and Django Rest Framework
=====
Đây là dự án Django về đơn vị hành chính Việt Nam. Dự án cung cấp mô hình để lưu trữ dữ liệu về các tỉnh/thành phố, quận/huyện, xã/phường của Việt Nam. Đồng thời tạo ra sẵn các endpoint để lấy dữ liệu.

Quick start
-----------

1. Add "rest_framework", "vi_address" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'vi_address',
    ]


2. Include the "vi_address" URLconf in your project urls.py like this::

    path('api/addresss/', include('vi_address.urls')),

3. Run "``python manage.py migrate``" to create the vi_address models.

4. Run "``python manage.py insert_data --datatype=city``" to insert data cities.

5. Run "``python manage.py insert_data --datatype=district``" to insert data districts.

6. Run "``python manage.py insert_data --datatype=ward``" to insert data wards.
