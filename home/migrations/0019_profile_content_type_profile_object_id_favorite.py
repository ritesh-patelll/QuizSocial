# Generated by Django 4.1.3 on 2023-04-30 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('home', '0018_profile_blocked_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='profile',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.profile')),
            ],
            options={
                'unique_together': {('profile', 'content_type', 'object_id')},
            },
        ),
    ]
