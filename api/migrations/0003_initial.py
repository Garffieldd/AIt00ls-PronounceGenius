# Generated by Django 4.1.13 on 2024-03-30 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0002_auto_20240330_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
                ('pronunciation', models.CharField(max_length=100)),
                ('correct', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='UserAudioInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=40, unique=True, verbose_name='email')),
                ('max_streak', models.IntegerField()),
                ('trys', models.ManyToManyField(to='api.trys')),
            ],
        ),
    ]
