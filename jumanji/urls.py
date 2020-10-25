from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

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
    path('companies/<int:id_company>', views.company_view, name='one_company'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('vacancies/<int:vacancy_id>/send', views.send_view, name='send'),
    path('mycompany', views.own_company, name='mycompany'),
    path('mycompany_create', views.create_own_company, name='mycompany_create'),
    path('mycompany/vacancies', views.vacancies_list_mycompany_view, name='mycompany_vacancies'),
    path('mycompany/vacancies/<int:vacancy_id>', views.vacancy_edit_view, name='mycompany_vacancy_edit'),
    path('mycompany/vacancies/create', views.vacancy_create_view, name='vacancy_generate'),
    path('myresume', views.own_resume, name='myresume'),
    path('myresume_create', views.resume_create_view, name='myresume_create'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
