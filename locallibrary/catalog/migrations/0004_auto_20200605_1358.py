# Generated by Django 2.2.12 on 2020-06-05 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20200605_0153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['title'], 'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
    ]
