from django.contrib import admin
from core.models import *
from .models import ResumenEquipo
from django.db.models.signals import post_save
from django.dispatch import receiver
from more_admin_filters import *
from django.utils.html import format_html

class PitcheoAdmin(admin.ModelAdmin):
    list_filter = ["liga_id", "campeonato", "categoria", "grupo", "juego", "equipo", "jugador_id"]
    # list_display = (
    #     "jugador_id", "juego"
    # )
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['jugador_id'].queryset = Jugador.objects.filter(tipo='Pitcher')
        return super(PitcheoAdmin, self).render_change_form(request, context, *args, **kwargs)
     
class BateoAdmin(admin.ModelAdmin):
    list_filter = ["liga_id", "campeonato", "categoria", "grupo", "juego", "equipo", "jugador_id"]
    
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['jugador_id'].queryset = Jugador.objects.filter(tipo='Bateador')
        return super(BateoAdmin, self).render_change_form(request, context, *args, **kwargs)
     
    # def save_model(self, request, obj, form, change):
    #     equipo_id = obj.equipo.id
    #     juego_id = obj.juego.id
    #     hits = obj.hits + obj.doble + obj.triple + obj.home_run
        
    #     juego = Juego.objects.get(id=juego_id)
        
    #     if juego.equipo_uno.id == equipo_id:
    #         juego.carrera_uno += obj.carrera
    #         juego.hits_uno += hits
    #     else:
    #         juego.carrera_dos += obj.carrera
    #         juego.hits_dos += hits
            
    #     juego.save()        
        
    #     super().save_model(request, obj, form, change)

class EquipoAdmin(admin.ModelAdmin):
    list_filter = ["liga_id", "campeonato", "categoria", "grupo"]
    list_display = (
        "equipo", "grupo", "categoria", "campeonato", "liga_id"
    )
    @receiver(post_save, sender = Equipo)
    def guardar_resumen(sender, instance, created, **kwargs):       
        resumen = ResumenEquipo()
        resumen.liga_id_id = instance.liga_id.id
        resumen.campeonato_id = instance.campeonato.id
        resumen.categoria_id = instance.categoria.id
        resumen.grupo_id = instance.grupo.id
        resumen.equipo_id = instance.id
        resumen.save() 
        return True
   
    
class JuegoAdmin(admin.ModelAdmin): 
    def opciones(self, obj):
        return format_html(
            '<a class="button" href="/admin/core/bateo/add/">Agregar bateo</a>',
            # '<a class="button" href="{}">Agregar bateo</a>',
            # reverse('admin:account-deposit', args=[obj.pk]),
            # reverse('admin:account-withdraw', args=[obj.pk]),
        )    
    list_filter = ["liga_id", "campeonato", "categoria", "grupo", "equipo_uno", "grupob", "equipo_dos"]
    list_display = (
        "__str__","liga_id","campeonato", "categoria", "grupo", "equipo_uno", "grupob", "equipo_dos",
        "opciones"
    )
    opciones.short_description = 'Opciones'
    
    
    
    def save_model(self, request, obj, form, change):
        equipo_uno = obj.equipo_uno
        equipo_dos = obj.equipo_dos
        carrera_uno = obj.carrera_uno
        carrera_dos = obj.carrera_dos
        
        resumen_equipo_uno = ResumenEquipo.objects.get(equipo=equipo_uno.id)
        resumen_equipo_dos = ResumenEquipo.objects.get(equipo=equipo_dos.id)
        
        if obj.finalizado:        
            if carrera_uno == carrera_dos:
                resumen_equipo_uno.empatados = resumen_equipo_uno.empatados + 1
                resumen_equipo_dos.empatados = resumen_equipo_dos.empatados + 1
                resumen_equipo_uno.save()
                resumen_equipo_dos.save()
            elif carrera_uno > carrera_dos:
                resumen_equipo_uno.ganados = resumen_equipo_uno.ganados + 1
                resumen_equipo_uno.save()
                resumen_equipo_dos.perdidos = resumen_equipo_dos.perdidos + 1
                resumen_equipo_dos.save()
            elif carrera_dos > carrera_uno:
                resumen_equipo_dos.ganados = resumen_equipo_dos.ganados + 1
                resumen_equipo_dos.save()
                resumen_equipo_uno.perdidos = resumen_equipo_uno.perdidos + 1
                resumen_equipo_dos.save()
                
            resumen_equipo_uno.jugados = resumen_equipo_uno.jugados + 1
            resumen_equipo_dos.jugados = resumen_equipo_dos.jugados + 1
            resumen_equipo_uno.save()
            resumen_equipo_dos.save()            
            
        super().save_model(request, obj, form, change)

class LigaAdmin(admin.ModelAdmin):
    list_filter = ["nombre", "periodo", "anno", "responsable"]
    list_display = (
        "nombre", "titulo_uno", "periodo", "anno", "responsable"
    )
    
class CampeonatoAdmin(admin.ModelAdmin):
    list_filter = ["liga_id", "nombre"]
    list_display = (
        "nombre", "liga_id"
    )
    
class GrupoAdmin(admin.ModelAdmin):
    list_filter = ["liga_id", "campeonato", "categoria", "nombre"]
    list_display = (
        "nombre", "categoria", "campeonato", "liga_id"
    )
    
class JugadorAdmin(admin.ModelAdmin):
    list_filter = ["liga_id", "campeonato", "categoria", "grupo", "equipo"]
    list_display = (
        "tipo", "nombre", "equipo", "grupo", "categoria", "campeonato", "liga_id"
    )

class CategoriaAdmin(admin.ModelAdmin):
    list_filter = ["liga_id", "campeonato", "nombre"]
    list_display = (
        "nombre", "campeonato", "liga_id"
    )

admin.site.register(Equipo, EquipoAdmin)
admin.site.register(Juego, JuegoAdmin)
admin.site.register(Liga,LigaAdmin)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Campeonato, CampeonatoAdmin)
admin.site.register(Jugador,JugadorAdmin)
admin.site.register(Pitcheo,PitcheoAdmin)
admin.site.register(Bateo, BateoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(ResumenEquipo)
