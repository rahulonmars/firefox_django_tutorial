# Generated by Django 2.2.12 on 2020-06-05 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20200605_1358'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
    ]