# Generated by Django 3.0.4 on 2020-10-25 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jumanji', '0002_auto_20201024_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('surname', models.CharField(max_length=150)),
                ('status', models.CharField(choices=[('NOTFIND', 'Не ищу работу'), ('GUESS', 'Рассматриваю предложения'), ('FIND', 'Ищу работу')], default='NOTFIND', max_length=25)),
                ('salary', models.IntegerField()),
                ('grade', models.CharField(choices=[('STAGE', 'Стажер'), ('JUNIOR', 'Джуниор'), ('MIDDLE', 'Миддл'), ('SENIOR', 'Синьор'), ('LEAD', 'Лид')], default='STAGE', max_length=25)),
                ('education', models.CharField(max_length=500)),
                ('experience', models.CharField(max_length=500)),
                ('portfolio', models.CharField(max_length=50)),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resumes', to='jumanji.Specialty')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resumes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]