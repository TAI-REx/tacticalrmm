# Generated by Django 3.2.6 on 2021-10-10 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0017_auto_20210417_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='created_by',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='modified_by',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='created_by',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='modified_by',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]