# Generated by Django 4.2.13 on 2024-07-23 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tamimi_admin', '0017_alter_deviceordermodel_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceordermodel',
            name='sortno',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
