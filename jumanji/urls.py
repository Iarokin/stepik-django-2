from django.contrib import admin
from django.urls import path

from jumanji import views
from jumanji.views import custom_handler404, custom_handler500

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_view, name='main_page'),
    path('vacancies/cat/<str:code_specialty>', views.vacancies_of_specialty_view, name='one_specialty'),
    path('vacancies/<int:id_vacancy>', views.vacancy_on_id_view, name='one_vacancy'),
    path('vacancies/', views.all_vacancy_view, name='all_vacancies'),
    path('companies/', views.all_companies_view, name='all_companies'),
    path('companies/<int:id_company>', views.company_view, name='one_company')
]
