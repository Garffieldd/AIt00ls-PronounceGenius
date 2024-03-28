# Generated by Django 5.0.3 on 2024-03-28 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAudioInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio', models.FileField(upload_to='audio/')),
                ('word', models.CharField(max_length=100)),
                ('streak', models.IntegerField()),
            ],
        ),
    ]