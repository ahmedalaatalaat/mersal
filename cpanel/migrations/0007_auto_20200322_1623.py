# Generated by Django 2.2 on 2020-03-22 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpanel', '0006_auto_20200322_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main_category',
            name='image',
            field=models.ImageField(default='img/Categories/category.png', upload_to='img/Categories'),
        ),
    ]
