# Generated by Django 5.2.3 on 2025-07-02 07:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webinar', '0023_alter_responsequestionaire_webinar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webinarattendees',
            name='webinar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendees', to='webinar.webinar'),
        ),
    ]
