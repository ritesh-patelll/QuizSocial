from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        TrigramExtension(),
    ]