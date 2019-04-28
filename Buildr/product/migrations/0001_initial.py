# Generated by Django 2.2 on 2019-04-28 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gpu',
            fields=[
                ('id', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('model', models.CharField(blank=True, max_length=10, null=True)),
                ('brand', models.CharField(blank=True, max_length=6, null=True)),
                ('vendor', models.CharField(blank=True, max_length=30, null=True)),
                ('image', models.CharField(blank=True, max_length=200, null=True)),
                ('min_price', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'gpu',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Motherboard',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('brand', models.CharField(blank=True, max_length=5, null=True)),
                ('chipset', models.CharField(max_length=20)),
                ('vendor', models.CharField(max_length=20)),
                ('socket', models.CharField(max_length=20)),
                ('image', models.CharField(blank=True, max_length=200, null=True)),
                ('min_price', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'motherboard',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Processor',
            fields=[
                ('id', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('brand', models.CharField(blank=True, max_length=5, null=True)),
                ('series', models.CharField(max_length=10)),
                ('gen', models.IntegerField()),
                ('socket', models.CharField(max_length=20)),
                ('codename', models.CharField(max_length=20)),
                ('unlocked', models.CharField(max_length=3)),
                ('image', models.CharField(blank=True, max_length=200, null=True)),
                ('min_price', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'processor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('category', models.CharField(blank=True, max_length=30, null=True)),
                ('image', models.CharField(blank=True, max_length=300, null=True)),
                ('min_price', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'product',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ram',
            fields=[
                ('id', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('brand', models.CharField(blank=True, max_length=30, null=True)),
                ('size', models.CharField(blank=True, max_length=5, null=True)),
                ('rate', models.CharField(blank=True, max_length=4, null=True)),
                ('speed', models.CharField(blank=True, max_length=7, null=True)),
                ('image', models.CharField(blank=True, max_length=200, null=True)),
                ('min_price', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ram',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GpuPrices',
            fields=[
                ('id', models.ForeignKey(db_column='id', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='product.Gpu')),
                ('price', models.IntegerField(blank=True, null=True)),
                ('link', models.CharField(max_length=200)),
                ('seller', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'gpu_prices',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MotherboardPrices',
            fields=[
                ('id', models.ForeignKey(db_column='id', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='product.Motherboard')),
                ('price', models.IntegerField(blank=True, null=True)),
                ('link', models.CharField(max_length=200)),
                ('seller', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'motherboard_prices',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProcessorPrices',
            fields=[
                ('id', models.ForeignKey(db_column='id', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='product.Processor')),
                ('price', models.IntegerField(blank=True, null=True)),
                ('link', models.CharField(max_length=200)),
                ('seller', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'processor_prices',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RamPrices',
            fields=[
                ('id', models.ForeignKey(db_column='id', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='product.Ram')),
                ('price', models.IntegerField(blank=True, null=True)),
                ('link', models.CharField(max_length=200)),
                ('seller', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'ram_prices',
                'managed': False,
            },
        ),
    ]
