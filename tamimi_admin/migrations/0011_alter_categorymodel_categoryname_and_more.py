# Generated by Django 5.0.6 on 2024-06-13 10:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tamimi_admin', '0010_alter_devicemodel_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorymodel',
            name='categoryname',
            field=models.CharField(editable=False, max_length=250),
        ),
        migrations.AlterField(
            model_name='categorymodel',
            name='catid',
            field=models.CharField(editable=False, max_length=250),
        ),
        migrations.AlterField(
            model_name='categorymodel',
            name='handle',
            field=models.CharField(editable=False, max_length=250),
        ),
        migrations.AlterField(
            model_name='devicemodel',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tamimi_admin.categorymodel'),
        ),
    ]
