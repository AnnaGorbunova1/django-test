# Generated by Django 4.1.7 on 2023-03-06 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangotest', '0006_alter_item_parent_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemstree',
            name='parent_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='itemstree_parent', to='djangotest.item'),
        ),
    ]
