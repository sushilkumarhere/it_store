# Generated by Django 4.0.1 on 2022-01-05 05:03

from django.db import migrations, models
import stock.models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0020_alter_itempurchase_item_invoice_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itempurchase',
            name='item_invoice_file',
            field=models.FileField(blank=True, help_text='Maximum file size allowed is 300KB', upload_to='invoice', validators=[stock.models.validate_file_size]),
        ),
    ]