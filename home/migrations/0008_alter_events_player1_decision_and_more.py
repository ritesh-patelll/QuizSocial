# Generated by Django 4.1.3 on 2023-04-03 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_events_event_type_events_event_wiki_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='player1_decision',
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='player2_decision',
            field=models.BooleanField(default=None, null=True),
        ),
    ]
