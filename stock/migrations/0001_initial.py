# Generated by Django 4.0.2 on 2022-02-26 12:48

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import stock.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ac_block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='InstituteName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Inst_name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['Inst_name'],
            },
        ),
        migrations.CreateModel(
            name='ItemModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ItemName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('item_image', models.ImageField(blank=True, help_text='Maximum file size allowed is 100KB', upload_to='item-pic', validators=[stock.models.validate_image])),
            ],
            options={
                'ordering': ['item_name'],
            },
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['room_type'],
            },
        ),
        migrations.CreateModel(
            name='ItemScrap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_scarp_date', models.DateField(blank=True, null=True)),
                ('item_configuration', models.CharField(max_length=100, verbose_name='Items Specifications')),
                ('purchase_date', models.DateField(blank=True, null=True)),
                ('scrap_type', models.CharField(choices=[('SCRAP', 'SCRAP'), ('DONATE', 'DONATE')], default='SCRAP', max_length=10, verbose_name='Scrap Type')),
                ('scrap_vendor', models.CharField(max_length=100, verbose_name='Vendor Name')),
                ('vendor_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('item_qty', models.IntegerField()),
                ('item_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.itemmodel')),
                ('item_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.itemname')),
            ],
            options={
                'verbose_name': 'Item Scarp',
            },
        ),
        migrations.CreateModel(
            name='ItemPurchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_purchase_date', models.DateField()),
                ('item_sl', models.CharField(max_length=100)),
                ('item_configuration', models.CharField(max_length=100, verbose_name='Items Specifications')),
                ('item_vendor', models.CharField(max_length=100, verbose_name='Vendor Name')),
                ('item_invoice', models.CharField(max_length=100, verbose_name='Invoice No')),
                ('item_invoice_file', models.FileField(blank=True, help_text='Maximum file size allowed is 300KB', upload_to='invoice', validators=[stock.models.validate_file_size])),
                ('item_price', models.CharField(max_length=100, verbose_name='Price')),
                ('item_qty', models.IntegerField()),
                ('item_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.itemmodel')),
                ('item_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.itemname')),
            ],
            options={
                'verbose_name': 'Item Purchase',
            },
        ),
        migrations.AddField(
            model_name='itemmodel',
            name='item_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stock.itemname'),
        ),
        migrations.CreateModel(
            name='ItemDist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_configuration', models.CharField(max_length=100, verbose_name='Items Specifications')),
                ('purchase_date', models.DateField(blank=True, null=True)),
                ('room', models.CharField(max_length=100, verbose_name='Room No')),
                ('user', models.CharField(blank=True, max_length=100)),
                ('item_qty', models.IntegerField()),
                ('act', models.IntegerField(default=0, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('acblock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.ac_block', verbose_name='Academic Block')),
                ('inst', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.institutename', verbose_name='Institute Name')),
                ('item_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.itemmodel')),
                ('item_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.itemname')),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.roomtype')),
            ],
            options={
                'verbose_name': 'Item Distribution',
            },
        ),
    ]
