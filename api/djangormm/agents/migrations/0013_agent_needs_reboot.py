# Generated by Django 3.0 on 2019-12-08 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0012_remove_agent_patches_pending'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='needs_reboot',
            field=models.BooleanField(default=False),
        ),
    ]
