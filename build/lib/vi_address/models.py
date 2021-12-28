from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    name_with_type = models.CharField(max_length=255)
    code = models.IntegerField()

    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.name_with_type


class District(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    name_with_type = models.CharField(max_length=255)
    path = models.CharField(max_length=500)
    path_with_type = models.CharField(max_length=1000)
    code = models.IntegerField()
    parent_code = models.ForeignKey(City, on_delete=models.CASCADE, related_name='districts')

    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.name_with_type


class Ward(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    name_with_type = models.CharField(max_length=255)
    path = models.CharField(max_length=500)
    path_with_type = models.CharField(max_length=1000)
    code = models.IntegerField()
    parent_code = models.ForeignKey(District, on_delete=models.CASCADE, related_name='wards')

    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.name_with_type
