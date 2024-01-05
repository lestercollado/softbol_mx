from django.urls import path

from . import views

urlpatterns = [
    path('', views.bateo_general_view, name='reporte_bg'),
    path('reporte_ea', views.estado_actual_view, name='reporte_ea'),
    path('reporte_bd', views.bateo_dpto_view, name='reporte_bd'),
    path('reporte_pg', views.pitcheo_ganados_view, name='reporte_pg'),
    path('reporte_pc', views.pitcheo_carreras_view, name='reporte_pc'),
    path('reporte_pp', views.pitcheo_ponches_view, name='reporte_pp'),
    path("bateo_general", views.bateo_general, name="bateo_general"),
    path("bateo_dpto", views.bateo_dpto, name="bateo_dpto"),
    path("pitcheo_ganados_perdidos", views.pitcheo_ganados_perdidos, name="pitcheo_ganados_perdidos"),
    path("pitcheo_carreras_limpias", views.pitcheo_carreras_limpias, name="pitcheo_carreras_limpias"),
    path("pitcheo_ponches", views.pitcheo_ponches, name="pitcheo_ponches"),
    path("estado_actual", views.reporte_estado_actual, name="reporte_estado_actual")
]
