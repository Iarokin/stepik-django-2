from jumanji import models, data


def generate():
    company_on_start = models.Company.objects.all()
    specialty_on_start = models.Specialty.objects.all()
    vacancy_on_start = models.Vacancy.objects.all()
    company_on_start.delete()
    specialty_on_start.delete()
    vacancy_on_start.delete()
    counter_id = 0
    for i in data.companies:
        company = models.Company.objects.create(
            id=counter_id,
            name=i['name'],
            location=i['location'],
            logo="https://place-hold.it/130x80",
            description=i['description'],
            employee_count=i['employee_count'],
        )
        counter_id = counter_id + 1
        company.save
    counter_id = 0
    for i in data.specialties:
        specialty = models.Specialty.objects.create(
            id=counter_id,
            code=i['code'],
            title=i['title'],
            picture="https://place-hold.it/100x60"
        )
        counter_id = counter_id + 1
        specialty.save
    counter_id = 0
    for i in data.vacancies:
        vacancy = models.Vacancy.objects.create(
            id=counter_id,
            title=i['title'],
            skills=i['skills'],
            description=i['description'],
            salary_min=i['salary_min'],
            salary_max=i['salary_max'],
            published_at=i['published_at'],
            specialty=models.Specialty.objects.get(code=i['specialty']),
            company=models.Company.objects.get(name=i['company'])
        )
        counter_id = counter_id + 1
        vacancy.save
