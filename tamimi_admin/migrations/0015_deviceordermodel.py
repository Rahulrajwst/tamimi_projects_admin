# Generated by Django 4.2.13 on 2024-07-17 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tamimi_admin', '0014_alter_parentsectionmodel_parentsectionimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceOrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tamimi_admin.devicemodel')),
            ],
        ),
    ]
