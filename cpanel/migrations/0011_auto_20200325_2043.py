# Generated by Django 2.2 on 2020-03-25 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpanel', '0010_auto_20200323_0009'),
    ]

    operations = [
        migrations.RenameField(
            model_name='main_category',
            old_name='name',
            new_name='english_name',
        ),
        migrations.RenameField(
            model_name='sub_category',
            old_name='name',
            new_name='english_name',
        ),
        migrations.AddField(
            model_name='main_category',
            name='arabic_name',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AddField(
            model_name='sub_category',
            name='arabic_name',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AlterUniqueTogether(
            name='sub_category',
            unique_together=set(),
        ),
    ]
