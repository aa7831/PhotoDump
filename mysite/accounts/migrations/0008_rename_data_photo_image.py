# Generated by Django 5.0.4 on 2024-04-23 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_photo_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='data',
            new_name='image',
        ),
    ]
