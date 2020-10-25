import os
import django
from jumanji import models, data
os.environ["DJANGO_SETTINGS_MODULE"] = 'conf.settings'
django.setup()

if __name__ == '__main__':
    company_on_start = models.Company.objects.all()
    specialty_on_start = models.Specialty.objects.all()
    vacancy_on_start = models.Vacancy.objects.all()
    application_on_start = models.Application.objects.all()
    company_on_start.delete()
    specialty_on_start.delete()
    vacancy_on_start.delete()
    application_on_start.delete()
    counter_id = 0
    for field_of_model in data.companies:
        company = models.Company.objects.create(
            id=counter_id,
            name=field_of_model['name'],
            location=field_of_model['location'],
            logo='logos/logo' + str(counter_id + 1) + '.png',
            description=field_of_model['description'],
            employee_count=field_of_model['employee_count'],
        )
        counter_id = counter_id + 1
    counter_id = 0
    for field_of_model in data.specialties:
        specialty = models.Specialty.objects.create(
            id=counter_id,
            code=field_of_model['code'],
            title=field_of_model['title'],
            picture='specialties/specty_' + field_of_model['code'] + '.png'
        )
        counter_id = counter_id + 1
    counter_id = 0
    for field_of_model in data.vacancies:
        vacancy = models.Vacancy.objects.create(
            id=counter_id,
            title=field_of_model['title'],
            skills=field_of_model['skills'],
            description=field_of_model['description'],
            salary_min=field_of_model['salary_min'],
            salary_max=field_of_model['salary_max'],
            published_at=field_of_model['published_at'],
            specialty=models.Specialty.objects.get(code=field_of_model['specialty']),
            company=models.Company.objects.get(name=field_of_model['company'])
        )
        counter_id = counter_id + 1
