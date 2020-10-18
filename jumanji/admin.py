from django.contrib import admin

from jumanji.models import Specialty, Vacancy, Company


@admin.register(Specialty, Vacancy, Company)
class JumanjiAdmin(admin.ModelAdmin):
    pass
