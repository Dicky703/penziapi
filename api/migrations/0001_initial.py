# Generated by Django 5.0.2 on 2024-02-14 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MessageFrom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msisdn', models.CharField(max_length=15)),
                ('message_content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MessageTo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_code', models.CharField(max_length=6)),
                ('response_content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('county', models.CharField(max_length=255)),
                ('town', models.CharField(max_length=255)),
                ('msisdn', models.CharField(max_length=15)),
                ('level_of_education', models.CharField(blank=True, max_length=255, null=True)),
                ('profession', models.CharField(blank=True, max_length=255, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=50, null=True)),
                ('religion', models.CharField(blank=True, max_length=50, null=True)),
                ('ethnicity', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField()),
                ('myself', models.TextField()),
                ('registration_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
