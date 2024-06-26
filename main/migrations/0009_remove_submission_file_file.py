# Generated by Django 5.0.2 on 2024-04-10 05:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_submission_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='file',
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='submissions/')),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.submission')),
            ],
        ),
    ]
