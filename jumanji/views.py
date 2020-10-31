from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from datetime import datetime


from jumanji import models, services, forms
from conf import settings


def main_view(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('search', kwargs={'query': request.POST['search_object']}))
    else:
        search_form = forms.SearchForm()
        specializations = models.Specialty.objects.all()
        companies = models.Company.objects.all()
        count_vacancies_for_all_specializations = services.count_vacancies_for_all_specializations()
        count_vacancies_for_all_companies = services.count_vacancies_for_all_companies()
        return render(request, 'index.html', context={
            'specializations': specializations,
            'companies': companies,
            'count_vacancies_for_all_specializations': count_vacancies_for_all_specializations,
            'count_vacancies_for_all_companies': count_vacancies_for_all_companies,
            'form': search_form
        })


def register_view(request):
    alert_text = ''
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            User.objects.create_user(
                username=register_form['username'].value(),
                first_name=register_form['first_name'].value(),
                last_name=register_form['last_name'].value(),
                password=register_form['password'].value()
            )
            return HttpResponseRedirect('/login')
        else:
            alert_text = "Использованы недопустимые данные в логине или пароле"
            register_form = forms.RegisterForm()
            return render(request, 'register.html', context={
                'register_form': register_form,
                'alert_text': alert_text
            })
    else:
        register_form = forms.RegisterForm()
        return render(request, 'register.html', context={
            'register_form': register_form,
            'alert_text': alert_text
        })


def login_view(request):
    alert_text = ''
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form['username'].value()
            password = login_form['password'].value()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                alert_text = 'Неверный логин или пароль'
                return render(request, 'login.html', context={
                    'login_form': login_form,
                    'alert_text': alert_text
                })
        else:
            alert_text = 'Неверный логин или пароль'
            return render(request, 'login.html', context={
                'login_form': login_form,
                'alert_text': alert_text
            })
    else:
        login_form = forms.LoginForm()
        return render(request, 'login.html', context={
            'login_form': login_form,
            'alert_text': alert_text
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def vacancies_of_specialty_view(request, code_specialty):
    input_specialty = models.Specialty.objects.filter(code=code_specialty).count()
    if input_specialty == 0:
        raise Http404
    id_specialty = getattr(models.Specialty.objects.get(code=code_specialty), 'id')
    specialty_name = getattr(models.Specialty.objects.get(code=code_specialty), 'title')
    vacancies = models.Vacancy.objects.filter(specialty=id_specialty)
    count_vacancies = models.Vacancy.objects.filter(specialty=id_specialty).count()
    return render(request, 'vacancies.html', context={
        'vacancies': vacancies,
        'count_vacancies': count_vacancies,
        'specialty_name': specialty_name,
    })


def vacancy_on_id_view(request, id_vacancy):
    if request.method == 'POST':
        application_form = forms.ApplicationForm(request.POST)
        if application_form.is_valid():
            application = models.Application.objects.create(
                written_username=application_form['written_username'].value(),
                written_phone=application_form['written_phone'].value(),
                written_cover_letter=application_form['written_cover_letter'].value(),
                vacancy=models.Vacancy.objects.get(id=id_vacancy),
                user=request.user
            )
            application.save()
            return HttpResponseRedirect(reverse('send', kwargs={'vacancy_id': id_vacancy}))
        else:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        application_form = forms.ApplicationForm()
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
            'form': application_form
        })


def send_view(request, vacancy_id):
    return render(request, 'sent.html')


def all_vacancy_view(request):
    vacancies = models.Vacancy.objects.all()
    companies = models.Company.objects.all()
    count_vacancies = models.Vacancy.objects.all().count()
    return render(request, 'vacancies.html', context={
        'vacancies': vacancies,
        'count_vacancies': count_vacancies,
        'specialty_name': "Все вакансии",
        'companies': companies
    })


def all_companies_view(request):
    companies = models.Company.objects.all()
    count_companies = models.Company.objects.all().count()
    return render(request, 'companies.html', context={
        'companies': companies,
        'count_companies': count_companies
    })


def company_view(request, id_company):
    input_company = models.Company.objects.filter(id=id_company).count()
    if input_company == 0:
        raise Http404
    company = models.Company.objects.get(id=id_company)
    company_name = models.Company.objects.get(id=id_company).name
    vacancies = models.Vacancy.objects.filter(company=id_company)
    count_vacancies = models.Vacancy.objects.filter(company=id_company).count()
    return render(request, 'company.html', context={
        'vacancies': vacancies,
        'count_vacancies': count_vacancies,
        'company_name': company_name,
        'company': company
    })


def own_company(request):
    alert_update = ''
    Anonymous = request.user.is_anonymous
    if Anonymous is False:
        if request.method == 'POST':
            company_form = forms.CompanyForm(request.POST, request.FILES)
            print(request.POST['logo'])
            models.Company.objects.filter(owner_id=User.objects.get(username=request.user).id).update(
                name=company_form['name'].value(),
                location=company_form['location'].value(),
                description=company_form['description'].value(),
                employee_count=company_form['employee_count'].value(),
                logo=settings.MEDIA_COMPANY_IMAGE_DIR + '/' + request.POST['logo']
            )
            alert_update = 'Информация о компании обновлена'
            company_by_user = models.Company.objects.get(owner_id=User.objects.get(username=request.user).id)
            return render(request, 'company-edit.html', context={
                'company': company_by_user,
                'form': company_form,
                'alert_update': alert_update
            })
        else:
            try:
                company_by_user = models.Company.objects.get(owner_id=User.objects.get(username=request.user).id)
                company_form = forms.CompanyForm()
                return render(request, 'company-edit.html', context={
                    'company': company_by_user,
                    'form': company_form,
                    'alert_update': alert_update
                })
            except ObjectDoesNotExist:
                return render(request, 'company-create.html')
    else:
        return HttpResponseRedirect(reverse('register'))


def create_own_company(request):
    Anonymous = request.user.is_anonymous
    if Anonymous is False:
        models.Company.objects.create(
            name='',
            location='',
            logo='logos/place_holder.png',
            description='',
            employee_count=0,
            owner=User.objects.get(username=request.user)
        )
        return HttpResponseRedirect(reverse('mycompany'))
    else:
        return HttpResponseRedirect(reverse('register'))


def vacancies_list_mycompany_view(request):
    Anonymous = request.user.is_anonymous
    if Anonymous is False:
        try:
            company_by_user_id = models.Company.objects.get(owner_id=User.objects.get(username=request.user).id).id
            vacncies_company_by_user = models.Vacancy.objects.filter(company=company_by_user_id)
            count_vacncies_company_by_user = models.Vacancy.objects.filter(company=company_by_user_id).count()
            return render(request, 'vacancy-list.html', context={
                'vacancies': vacncies_company_by_user,
                'count_vacancies': count_vacncies_company_by_user
            })
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('mycompany'))
    else:
        return HttpResponseRedirect(reverse('register'))


def vacancy_edit_view(request, vacancy_id):
    alert_update = ''
    specialties = models.Specialty.objects.all()
    Anonymous = request.user.is_anonymous
    if Anonymous is False:
        if request.method == 'POST':
            vacancy_form = forms.VacancyForm(request.POST)
            models.Vacancy.objects.filter(id=vacancy_id).update(
                title=vacancy_form['title'].value(),
                skills=vacancy_form['skills'].value(),
                description=vacancy_form['description'].value(),
                salary_min=vacancy_form['salary_min'].value(),
                salary_max=vacancy_form['salary_max'].value(),
                specialty=models.Specialty.objects.get(code=vacancy_form['specialty'].value())
            )
            alert_update = 'Информация о вакансии обновлена'
            applications = models.Application.objects.filter(vacancy=vacancy_id)
            count_applications = models.Application.objects.filter(vacancy=vacancy_id).count()
            my_vacancy = models.Vacancy.objects.get(id=vacancy_id)
            return render(request, 'vacancy-edit.html', context={
                'vacancy': my_vacancy,
                'applications': applications,
                'count_applications': count_applications,
                'form': vacancy_form,
                'alert_update': alert_update,
                'specialties': specialties
            })
        else:
            vacancy_form = forms.VacancyForm()
            try:
                my_vacancy = models.Vacancy.objects.get(id=vacancy_id)
                applications = models.Application.objects.filter(vacancy=vacancy_id)
                count_applications = models.Application.objects.filter(vacancy=vacancy_id).count()
                return render(request, 'vacancy-edit.html', context={
                    'vacancy': my_vacancy,
                    'applications': applications,
                    'count_applications': count_applications,
                    'form': vacancy_form,
                    'alert_update': alert_update,
                    'specialties': specialties
                })
            except ObjectDoesNotExist:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect(reverse('register'))


def vacancy_create_view(request):
    Anonymous = request.user.is_anonymous
    if Anonymous is False:
        vacancy = models.Vacancy.objects.create(
            title=' ',
            skills=' ',
            description=' ',
            salary_min=0,
            salary_max=0,
            published_at=datetime.now(tz=None),
            specialty=models.Specialty.objects.filter().first(),
            company=models.Company.objects.get(owner_id=User.objects.get(username=request.user).id)
        )
        vacancy.save()
        return HttpResponseRedirect(reverse('mycompany_vacancy_edit', kwargs={'vacancy_id': vacancy.id}))
    else:
        return HttpResponseRedirect(reverse('register'))


def own_resume(request):
    alert_update = ''
    specialties = models.Specialty.objects.all()
    Anonymous = request.user.is_anonymous
    if Anonymous is False:
        if request.method == 'POST':
            resume_form = forms.ResumeForm(request.POST, request.FILES)
            if resume_form.is_valid():
                models.Resume.objects.filter(user=User.objects.get(username=request.user).id).update(
                    name=resume_form['name'].value(),
                    surname=resume_form['surname'].value(),
                    status=resume_form['status'].value(),
                    salary=resume_form['salary'].value(),
                    specialty=models.Specialty.objects.get(code=resume_form['specialty'].value()),
                    grade=resume_form['grade'].value(),
                    education=resume_form['education'].value(),
                    experience=resume_form['experience'].value(),
                    portfolio=resume_form['portfolio'].value()
                )
                alert_update = 'Ваше резюме обновлено!'
                resume_by_user = models.Resume.objects.get(user=User.objects.get(username=request.user).id)
                return render(request, 'resume-edit.html', context={
                    'resume': resume_by_user,
                    'form': resume_form,
                    'alert_update': alert_update,
                    'specialties': specialties
                })
            else:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            try:
                resume_by_user = models.Resume.objects.get(user=User.objects.get(username=request.user).id)
                resume_form = forms.ResumeForm()
                return render(request, 'resume-edit.html', context={
                    'resume': resume_by_user,
                    'form': resume_form,
                    'alert_update': alert_update,
                    'specialties': specialties
                })
            except ObjectDoesNotExist:
                return render(request, 'resume-create.html')
    else:
        return HttpResponseRedirect(reverse('register'))


def resume_create_view(request):
    Anonymous = request.user.is_anonymous
    if Anonymous is False:
        resume = models.Resume.objects.create(
            user=User.objects.get(username=request.user),
            name='',
            surname='',
            status='NOTFIND',
            salary=0,
            specialty=models.Specialty.objects.filter().first(),
            grade='STAGE',
            education='',
            experience='',
            portfolio=''
        )
        resume.save()
        return HttpResponseRedirect(reverse('myresume'))
    else:
        return HttpResponseRedirect(reverse('register'))


def search_view(request, query):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('search', kwargs={'query': request.POST['search_object']}))
    search_result = models.Vacancy.objects.filter(
        Q(
            title__icontains=query
        ) | Q(
            skills__icontains=query
        ) | Q(
            description__icontains=query
        ) | Q(
            specialty__title__icontains=query
        ) | Q(
            company__name__icontains=query
        )
    )
    count_search_result = search_result.count
    return render(request, 'search.html', context={
        'vacancies': search_result,
        'count_vacancies': count_search_result,
        'query_search_words': query
    })


def custom_handler404(request, exception):
    return HttpResponseNotFound('Данной страницы не существует. Попробуйте перейти к другой :).')


def custom_handler500(request, *args, **argv):
    return HttpResponse('Ошибка на стороне сервера')
