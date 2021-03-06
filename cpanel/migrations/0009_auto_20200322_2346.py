# Generated by Django 2.2 on 2020-03-22 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cpanel', '0008_auto_20200322_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='assigned_agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cpanel.Agent'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='charitable_activity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cpanel.Sub_Category'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='contribution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cpanel.Contribution'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='donor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cpanel.Donor'),
        ),
    ]
