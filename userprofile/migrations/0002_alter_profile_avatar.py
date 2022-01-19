# Generated by Django 4.0.1 on 2022-01-05 08:02

from django.db import migrations, models
import userprofile.models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, help_text='Maximum file size allowed is 100KB', null=True, upload_to='customers/profiles/avatars/', validators=[userprofile.models.validate_image]),
        ),
    ]
