# Generated by Django 4.2.13 on 2024-08-13 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tamimi_admin', '0023_rename_childsection_sectionordermodel_normalsection'),
    ]

    operations = [
        migrations.CreateModel(
            name='FCMTokenModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_token', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
