# Generated by Django 4.1.7 on 2023-03-06 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangotest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemstree',
            name='parent_id',
        ),
    ]