# Generated by Django 4.1.3 on 2023-05-02 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_alter_events_player1_alter_events_player2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='events',
            name='player1',
        ),
        migrations.RemoveField(
            model_name='events',
            name='player2',
        ),
        migrations.DeleteModel(
            name='ManagingRooms',
        ),
        migrations.RemoveField(
            model_name='quiz_card',
            name='user',
        ),
        migrations.RemoveField(
            model_name='reported_question',
            name='user',
        ),
        migrations.DeleteModel(
            name='Reported_Question_Count',
        ),
        migrations.DeleteModel(
            name='requested_movie',
        ),
        migrations.DeleteModel(
            name='requested_series',
        ),
        migrations.DeleteModel(
            name='RoomMember',
        ),
        migrations.RemoveField(
            model_name='video_event_logs',
            name='user',
        ),
        migrations.RemoveField(
            model_name='videoeventpoints',
            name='user',
        ),
        migrations.AlterField(
            model_name='favorite',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Favorite_profile', to='home.profile'),
        ),
        migrations.DeleteModel(
            name='events',
        ),
        migrations.DeleteModel(
            name='Quiz_Card',
        ),
        migrations.DeleteModel(
            name='Reported_Question',
        ),
        migrations.DeleteModel(
            name='Video_Event_Logs',
        ),
        migrations.DeleteModel(
            name='VideoEventPoints',
        ),
    ]
