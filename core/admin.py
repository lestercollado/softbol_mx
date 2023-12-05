from django.contrib import admin
from core.models import *

class PitcheoAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['jugador_id'].queryset = Jugador.objects.filter(tipo='Pitcher')
         return super(PitcheoAdmin, self).render_change_form(request, context, *args, **kwargs)
     
class BateoAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['jugador_id'].queryset = Jugador.objects.filter(tipo='Bateador')
         return super(BateoAdmin, self).render_change_form(request, context, *args, **kwargs)
     
admin.site.register(Temporada)
admin.site.register(Equipo)
admin.site.register(Juego)
admin.site.register(Liga)
admin.site.register(Grupo)
admin.site.register(Campo)
admin.site.register(Jugador)
admin.site.register(Pitcheo,PitcheoAdmin)
admin.site.register(Bateo, BateoAdmin)
admin.site.register(Categoria)
