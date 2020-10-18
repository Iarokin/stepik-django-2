from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404

from jumanji import models, services, script_database

links = [
    {"title": "Вакансии", "link": "vacancies"},
    {"title": "Компании", "link": "companies"},
]
StartServer = True


def main_view(request):
    global StartServer
    if StartServer:
        script_database.generate()
        StartServer = False
    specializations = models.Specialty.objects.values()
    companies = models.Company.objects.values()
    count_vacancies_for_all_specializations = services.count_vacancies_for_all_specializations()
    count_vacancies_for_all_companies = services.count_vacancies_for_all_companies()
    return render(request, 'index.html', context={
        'specializations': specializations,
        'companies': companies,
        'count_vacancies_for_all_specializations': count_vacancies_for_all_specializations,
        'count_vacancies_for_all_companies': count_vacancies_for_all_companies,
        'links': links
    })


def vacancies_of_specialty_view(request, code_specialty):
    input_specialty = models.Specialty.objects.filter(code=code_specialty).count()
    if input_specialty == 0:
        raise Http404
    id_specialty = getattr(models.Specialty.objects.get(code=code_specialty), 'id')
    specialty_name = getattr(models.Specialty.objects.get(code=code_specialty), 'title')
    vacancies = models.Vacancy.objects.filter(specialty=id_specialty).values()
    count_vacancies = models.Vacancy.objects.filter(specialty=id_specialty).count()
    return render(request, 'vacancies.html', context={
        'vacancies': vacancies,
        'count_vacancies': count_vacancies,
        'specialty_name': specialty_name,
        'links': links
    })


def vacancy_on_id_view(request, id_vacancy):
    input_vacancy = models.Vacancy.objects.filter(id=id_vacancy).count()
    if input_vacancy == 0:
        raise Http404
    vacancy = models.Vacancy.objects.get(id=id_vacancy)
    company = getattr(vacancy, 'company')
    specialty = getattr(vacancy, 'specialty')
    return render(request, 'vacancy.html', context={
        'vacancy': vacancy,
        'company': company,
        'specialty': specialty,
        'links': links
    })


def all_vacancy_view(request):
    vacancies = models.Vacancy.objects.all().values()
    count_vacancies = models.Vacancy.objects.all().count()
    return render(request, 'vacancies.html', context={
        'vacancies': vacancies,
        'count_vacancies': count_vacancies,
        'specialty_name': "Все вакансии",
        'links': links
    })


def all_companies_view(request):
    companies = models.Company.objects.all().values()
    count_companies = models.Company.objects.all().count()
    return render(request, 'companies.html', context={
        'companies': companies,
        'count_companies': count_companies
    })


def company_view(request, id_company):
    input_company = models.Company.objects.filter(id=id_company).count()
    if input_company == 0:
        raise Http404
    company_name = getattr(models.Company.objects.get(id=id_company), 'name')
    vacancies = models.Vacancy.objects.filter(company=id_company).values()
    count_vacancies = models.Vacancy.objects.filter(company=id_company).count()
    return render(request, 'company.html', context={
        'vacancies': vacancies,
        'count_vacancies': count_vacancies,
        'company_name': company_name,
        'links': links
    })


def custom_handler404(request, exception):
    return HttpResponseNotFound('Данной страницы не существует. Попробуйте перейти к другой :).')


def custom_handler500(request, *args, **argv):
    return HttpResponse('Ошибка на стороне сервера')
