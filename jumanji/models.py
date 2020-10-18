from django.db import models


class Company (models.Model):
    name = models.CharField(max_length=25)
    location = models.CharField(max_length=25)
    logo = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    employee_count = models.IntegerField()


class Specialty (models.Model):
    code = models.CharField(max_length=15, unique=True)
    title = models.CharField(max_length=25, unique=True)
    picture = models.CharField(max_length=100)


class Vacancy(models.Model):
    title = models.CharField(max_length=25)
    skills = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies', unique=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies', unique=False)
