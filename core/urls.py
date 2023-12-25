from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("bateo_general", views.bateo_general, name="bateo_general"),
    path("bateo_dpto", views.bateo_dpto, name="bateo_dpto"),
    path("pitcheo_ganados_perdidos", views.pitcheo_ganados_perdidos, name="pitcheo_ganados_perdidos"),
    path("pitcheo_carreras_limpias", views.pitcheo_carreras_limpias, name="pitcheo_carreras_limpias"),
    path("pitcheo_ponches", views.pitcheo_ponches, name="pitcheo_ponches"),
    path("estado_actual", views.reporte_estado_actual, name="reporte_estado_actual")
]
