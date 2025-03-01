# Generated by Django 4.1.3 on 2023-05-02 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0027_remove_events_content_type_remove_events_player1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('uid', models.CharField(max_length=1000)),
                ('room_name', models.CharField(max_length=200)),
                ('insession', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='VideoEventPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0)),
                ('object_id', models.BigIntegerField()),
                ('accusation', models.CharField(blank=True, max_length=1000, null=True)),
                ('accused_ss', models.ImageField(blank=True, max_length=255, null=True, upload_to='')),
                ('previous_rank', models.IntegerField(default=0)),
                ('total_event_played', models.IntegerField(default=0)),
                ('average_points', models.FloatField(default=0.0)),
                ('accused_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accused_by', to='home.profile')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('playedwith', models.ManyToManyField(blank=True, related_name='played_with_users', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='VideoEventPoints_user', to='home.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Video_Event_Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(blank=True, null=True)),
                ('object_id', models.BigIntegerField()),
                ('event_taken_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('playedwith', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Video_Event_Logs_playedwith', to='home.profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Video_Event_Logs_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='requested_quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.BigIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ManyToManyField(related_name='requested_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reported_Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500)),
                ('problem', models.CharField(max_length=1000, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.BigIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Reported_Question_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz_Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.BigIntegerField()),
                ('correct_answers', models.IntegerField(default=0)),
                ('total_question', models.IntegerField(default=0)),
                ('card', models.ImageField(blank=True, max_length=255, null=True, upload_to='')),
                ('quiz_taken_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Quiz_Card_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ManagingRooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.BigIntegerField()),
                ('room_no', models.IntegerField()),
                ('people_count', models.IntegerField()),
                ('player1_isactive', models.BooleanField(default=False)),
                ('player2_isactive', models.BooleanField(default=False)),
                ('room_type', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ManagingRooms_player1_profile', to='home.profile')),
                ('player2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ManagingRooms_player2_profile', to='home.profile')),
            ],
        ),
        migrations.CreateModel(
            name='events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.BigIntegerField()),
                ('event_name', models.CharField(max_length=255)),
                ('event_link', models.CharField(max_length=255)),
                ('event_date_time', models.DateTimeField()),
                ('event_created_date_time', models.DateTimeField(auto_now_add=True)),
                ('player1_decision', models.BooleanField(default=None, null=True)),
                ('player2_decision', models.BooleanField(default=None, null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events_player1_profile', to='home.profile')),
                ('player2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events_player2_profile', to='home.profile')),
            ],
        ),
    ]
