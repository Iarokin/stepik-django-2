from jumanji import models


def count_vacancies_for_all_specializations():
    counters_dict_specializations = {
        id_specialty: models.Vacancy.objects.filter(specialty=id_specialty).count()
        for id_specialty in range(models.Specialty.objects.all().count())
    }
    return counters_dict_specializations


def count_vacancies_for_all_companies():
    counters_dict_companies = {
        id_company: models.Vacancy.objects.filter(company=id_company).count()
        for id_company in range(models.Company.objects.all().count())
    }
    return counters_dict_companies
