from django.db import models

class Gpu(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    model = models.CharField(max_length=10, blank=True, null=True)
    brand = models.CharField(max_length=6, blank=True, null=True)
    vendor = models.CharField(max_length=30, blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)
    min_price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gpu'
    def __str__(self):
        return (self.id + ' ' +  self.model  + ' ' + self.vendor )


class GpuPrices(models.Model):
    id = models.ForeignKey(Gpu, models.DO_NOTHING, db_column='id', primary_key=True)
    price = models.IntegerField(blank=True, null=True)
    link = models.CharField(max_length=200)
    seller = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = 'gpu_prices'
        unique_together = (('id', 'seller'))
    def __str__(self):
        return (self.id.id + ' ' + self.seller)


class Motherboard(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    brand = models.CharField(max_length=5, blank=True, null=True)
    chipset = models.CharField(max_length=20)
    vendor = models.CharField(max_length=20)
    socket = models.CharField(max_length=20)
    image = models.CharField(max_length=200, blank=True, null=True)
    min_price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'motherboard'
    def __str__(self):
        return (self.id + ' ' +  self.chipset  + ' ' + self.vendor)


class MotherboardPrices(models.Model):
    id = models.ForeignKey(Motherboard, models.DO_NOTHING, db_column='id', primary_key=True)
    price = models.IntegerField(blank=True, null=True)
    link = models.CharField(max_length=200)
    seller = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = 'motherboard_prices'
        unique_together = (('id', 'seller'))
    def __str__(self):
        return (self.id.id + ' ' + self.seller)


class Processor(models.Model):
    id = models.CharField(primary_key=True, max_length=7)
    brand = models.CharField(max_length=5, blank=True, null=True)
    series = models.CharField(max_length=10)
    gen = models.IntegerField()
    socket = models.CharField(max_length=20)
    codename = models.CharField(max_length=20)
    unlocked = models.CharField(max_length=3)
    image = models.CharField(max_length=200, blank=True, null=True)
    min_price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'processor'
    def __str__(self):
        return (self.id)
    


class ProcessorPrices(models.Model):
    id = models.ForeignKey(Processor, models.DO_NOTHING, db_column='id', primary_key=True)
    price = models.IntegerField(blank=True, null=True)
    link = models.CharField(max_length=200)
    seller = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = 'processor_prices'
        unique_together = (('id', 'seller'))
    def __str__(self):
        return (self.id.id + ' ' + self.seller)


class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    title = models.CharField(max_length=300, blank=True, null=True)
    category = models.CharField(max_length=30, blank=True, null=True)
    image = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'
    def __str__(self):
        return (self.title)


class Ram(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    brand = models.CharField(max_length=30, blank=True, null=True)
    size = models.CharField(max_length=5, blank=True, null=True)
    rate = models.CharField(max_length=4, blank=True, null=True)
    speed = models.CharField(max_length=7, blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)
    min_price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ram'
    def __str__(self):
        return (self.id + ' ' + self.brand + ' ' + self.size + ' ' + self.speed )


class RamPrices(models.Model):
    id = models.ForeignKey(Ram, models.DO_NOTHING, db_column='id', primary_key=True)
    price = models.IntegerField(blank=True, null=True)
    link = models.CharField(max_length=200)
    seller = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = 'ram_prices'
        unique_together = (('id', 'seller'))
    def __str__(self):
        return (self.id.id + ' ' + self.seller)