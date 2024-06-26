# Generated by Django 5.0.6 on 2024-06-08 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tamimi_admin', '0005_categorysectionmodel_delete_devicemodel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CategorySectionModel',
        ),
        migrations.AlterField(
            model_name='categoryinfomodel',
            name='categoryhomeimage',
            field=models.ImageField(null=True, upload_to='homeimages/'),
        ),
        migrations.AlterField(
            model_name='categoryinfomodel',
            name='categorysectionimage',
            field=models.ImageField(null=True, upload_to='sectionimages/'),
        ),
    ]
