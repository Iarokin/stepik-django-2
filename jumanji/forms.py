from django import forms

from jumanji import models


class ApplicationForm (forms.Form):
    written_username = forms.CharField(max_length=20, label='Вас зовут')
    written_phone = forms.CharField(max_length=20, label='Ваш телефон')
    written_cover_letter = forms.CharField(max_length=200, label='Сопроводительное письмо')


class RegisterForm (forms.Form):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())


class LoginForm (forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())


class CompanyForm(forms.Form):
    model = models.Company
    name = forms.CharField(max_length=25)
    location = forms.CharField(max_length=25)
    description = forms.CharField(max_length=100)
    logo = forms.FileField()
    employee_count = forms.IntegerField()


class VacancyForm(forms.Form):
    title = forms.CharField(max_length=25)
    skills = forms.CharField(max_length=100)
    description = forms.CharField(max_length=200)
    salary_min = forms.IntegerField()
    salary_max = forms.IntegerField()
    published_at = forms.DateField()
    specialty = forms.ModelChoiceField(models.Specialty.objects.all(), to_field_name='code')


class ResumeForm(forms.Form):
    status_by_work = (
        ('NOTFIND','Не ищу работу'),
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

    name = forms.CharField(max_length=150)
    surname = forms.CharField(max_length=150)
    status = forms.ChoiceField(choices=status_by_work)
    salary = forms.IntegerField()
    specialty = forms.ModelChoiceField(models.Specialty.objects.all(), to_field_name='code')
    grade = forms.ChoiceField(choices=qualifications)
    education = forms.CharField(max_length=500)
    experience = forms.CharField(max_length=500)
    portfolio = forms.CharField(max_length=50)


class SearchForm(forms.Form):
    search_objects=forms.CharField(max_length=100)
