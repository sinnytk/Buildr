from django.db import models

class Gpu(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    model = models.CharField(max_length=10, blank=True, null=True)
    brand = models.CharField(max_length=6, blank=True, null=True)
    vendor = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gpu'


class Motherboard(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    brand = models.CharField(max_length=5, blank=True, null=True)
    chipset = models.CharField(max_length=20)
    vendor = models.CharField(max_length=20)
    socket = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'motherboard'


class Processor(models.Model):
    id = models.CharField(primary_key=True, max_length=7)
    brand = models.CharField(max_length=5, blank=True, null=True)
    series = models.CharField(max_length=10)
    gen = models.IntegerField()
    socket = models.CharField(max_length=20)
    codename = models.CharField(max_length=20)
    unlocked = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'processor'


class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    title = models.CharField(max_length=300, blank=True, null=True)
    category = models.CharField(max_length=30, blank=True, null=True)
    image = models.CharField(max_length=300, blank=True, null=True)
    min_price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'


class ProductPrices(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    price = models.IntegerField(blank=True, null=True)
    link = models.CharField(max_length=200)
    seller = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_prices'
        unique_together = (('id', 'link'),)


class Ram(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    brand = models.CharField(max_length=30, blank=True, null=True)
    size = models.CharField(max_length=5, blank=True, null=True)
    rate = models.CharField(max_length=4, blank=True, null=True)
    speed = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ram'