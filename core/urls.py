from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("bateo_general", views.bateo_general, name="bateo_general"),
    path("bateo_dpto", views.bateo_dpto, name="bateo_dpto"),
    path("estado_actual", views.reporte_estado_actual, name="reporte_estado_actual")
]
