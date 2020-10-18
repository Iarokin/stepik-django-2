# Generated by Django 3.0.4 on 2020-10-17 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('location', models.CharField(max_length=25)),
                ('logo', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('employee_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15,  unique = True)),
                ('title', models.CharField(max_length=25,  unique = True)),
                ('picture', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('skills', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('salary_min', models.IntegerField()),
                ('salary_max', models.IntegerField()),
                ('published_at', models.DateField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='jumanji.Company', unique = False)),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='jumanji.Specialty', unique = False)),
            ],
        ),
    ]
