# Generated by Django 2.2.10 on 2021-08-28 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0014_auto_20210827_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itempurchase',
            name='item_purchase_date',
            field=models.DateField(),
        ),
    ]