# Generated by Django 4.1.3 on 2023-05-01 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_remove_events_event_created_date_time_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='events',
        ),
    ]
