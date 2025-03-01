# Generated by Django 3.1.3 on 2021-03-15 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DumDumSocialBotChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dumdumsocialbot_id', models.CharField(max_length=128, unique=True)),
                ('type', models.CharField(choices=[('private', 'private'), ('group', 'group'), ('supergroup', 'supergroup'), ('channel', 'channel')], max_length=128)),
                ('title', models.CharField(blank=True, max_length=512, null=True)),
                ('username', models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DumDumSocialBotUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dumdumsocialbot_id', models.CharField(max_length=128, unique=True)),
                ('is_bot', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(blank=True, max_length=128, null=True)),
                ('username', models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DumDumSocialBotState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('memory', models.TextField(blank=True, null=True, verbose_name='Memory in JSON format')),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('dumdumsocialbot_chat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dumdumsocialbot_states', to='dumdumsocialbot.dumdumsocialbotchat')),
                ('dumdumsocialbot_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dumdumsocialbot_states', to='dumdumsocialbot.dumdumsocialbotuser')),
            ],
            options={
                'unique_together': {('dumdumsocialbot_user', 'dumdumsocialbot_chat')},
            },
        ),
    ]
