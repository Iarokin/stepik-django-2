from django.db import models
from django.contrib.auth.models import User


class Company (models.Model):
    name = models.CharField(max_length=25)
    location = models.CharField(max_length=25)
    logo = models.ImageField(upload_to='logos')
    description = models.CharField(max_length=100)
    employee_count = models.IntegerField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="companies", blank=True, null=True)


class Specialty (models.Model):
    code = models.CharField(max_length=15, unique=True)
    title = models.CharField(max_length=25, unique=True)
    picture = models.ImageField(upload_to='specialties')


class Vacancy(models.Model):
    title = models.CharField(max_length=25)
    skills = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies', unique=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies', unique=False)


class Application(models.Model):
    written_username = models.CharField(max_length=20)
    written_phone = models.CharField(max_length=20)
    written_cover_letter = models.CharField(max_length=200)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")


class Resume(models.Model):
    status_by_work = (
        ('NOTFIND', 'Не ищу работу'),
        ('GUESS', 'Рассматриваю предложения'),
        ('FIND', 'Ищу работу'),
    )

    qualifications = (
        ('STAGE', 'Стажер'),
        ('JUNIOR', 'Джуниор'),
        ('MIDDLE', 'Миддл'),
        ('SENIOR', 'Синьор'),
        ('LEAD', 'Лид')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="resumes")
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    status = models.CharField(choices=status_by_work, default='NOTFIND', max_length=25)
    salary = models.IntegerField()
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='resumes', unique=False)
    grade = models.CharField(choices=qualifications, default='STAGE', max_length=25)
    education = models.CharField(max_length=500)
    experience = models.CharField(max_length=500)
    portfolio = models.CharField(max_length=50)
