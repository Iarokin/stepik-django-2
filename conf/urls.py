from django.contrib import admin
from django.urls import path, include

from jumanji.views import custom_handler404, custom_handler500

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jumanji.urls')),
]
