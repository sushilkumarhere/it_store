# Generated by Django 3.1.4 on 2021-03-04 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0006_auto_20210303_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemdist',
            name='user',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]