# Generated by Django 4.1.3 on 2023-04-01 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='event_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='events',
            name='event_wiki_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
