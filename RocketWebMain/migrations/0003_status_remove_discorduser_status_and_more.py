# Generated by Django 5.1.4 on 2025-01-11 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RocketWebMain', '0002_alter_discorduser_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='discorduser',
            name='status',
        ),
        migrations.AddField(
            model_name='discorduser',
            name='statuses',
            field=models.ManyToManyField(blank=True, to='RocketWebMain.status'),
        ),
    ]
