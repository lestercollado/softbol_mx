from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey, GroupedForeignKey

class Temporada(models.Model):
    nombre = models.CharField(max_length=50) 
    
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Temporada'
        verbose_name_plural = 'Temporadas'
        
class Bateo(models.Model):
    juego_id = models.ForeignKey('Juego', models.DO_NOTHING, db_column='juego_id', verbose_name="Juego")
    jugador_id = models.ForeignKey('Jugador', models.DO_NOTHING, db_column='jugador_id', verbose_name="Bateador")
    veces_bate = models.IntegerField(verbose_name="Veces al Bate")
    hits = models.IntegerField(verbose_name="Hits")
    doble = models.IntegerField(verbose_name="Dobles")
    triple = models.IntegerField(verbose_name="Triples")
    home_run = models.IntegerField(verbose_name="Home Run")
    carrera = models.IntegerField(verbose_name="Carreras")
    base_robada = models.IntegerField(verbose_name="Bases robadas")
    base_bola = models.IntegerField(verbose_name="Bases por bolas")
    ponche = models.IntegerField(verbose_name="Ponches")
    
    def __str__(self):
        return self.jugador_id.nombre + " en el " + str(self.juego_id)

    def clean(self, *args, **kwargs):
        veces_bate = self.veces_bate
        hits = self.hits
        doble = self.doble
        triple = self.triple
        home_run = self.home_run
        base_bola = self.base_bola
        ponche = self.ponche
        if veces_bate < hits:
            raise ValidationError('No puede tener más Hits que veces al bate')
        if veces_bate < doble:
            raise ValidationError('No puede tener más Dobles que veces al bate')
        if veces_bate < triple:
            raise ValidationError('No puede tener más Triples que veces al bate')
        if veces_bate < home_run:
            raise ValidationError('No puede tener más HomeRuns que veces al bate')
        if veces_bate < base_bola:
            raise ValidationError('No puede tener más Base por bolas que veces al bate')
        if veces_bate < ponche:
            raise ValidationError('No puede tener más Ponches que veces al bate')
        if veces_bate < (hits+doble+triple+home_run+base_bola+ponche):
            raise ValidationError('La suma de todas las conexiones, ponches y bases por bolas debe ser menor o igual a las veces al bate')
        super().clean(*args, **kwargs)    
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Bateo'
        verbose_name_plural = 'Bateos'
        
class Campo(models.Model):
    nombre = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Campo'
        verbose_name_plural = 'Campos'
        
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        

class Liga(models.Model):
    temporada_id = models.ForeignKey('Temporada', models.DO_NOTHING, db_column='temporada_id', verbose_name="Temporada")
    categoria_id = models.ForeignKey('Categoria', models.DO_NOTHING, db_column='categoria_id', verbose_name="Categoría")
    nombre = models.CharField(max_length=200)
    titulo_uno = models.CharField(max_length=200)
    titulo_dos = models.CharField(max_length=200)
    periodo = models.CharField(max_length=200, verbose_name="Período")
    logo = models.ImageField()
    anno = models.IntegerField(verbose_name="Año")
    responsable = models.CharField(max_length=100)    
    
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Liga'
        verbose_name_plural = 'Ligas'
        
class Grupo(models.Model):
    liga = models.ForeignKey(Liga, models.DO_NOTHING)
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'


class Equipo(models.Model):
    # liga = models.ForeignKey(Liga, models.DO_NOTHING)
    # grupo_id = models.ForeignKey('Grupo', models.DO_NOTHING, db_column='grupo_id', verbose_name="Grupo")
    grupo = ChainedForeignKey(
        Grupo,
        chained_field="liga_id",
        chained_model_field="liga_id",
        show_all=False,
        auto_choose=True,
        sort=True)
    grupo = GroupedForeignKey(Grupo, "liga")
    equipo = models.CharField(max_length=200)
    
    def __str__(self):
        return self.equipo

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        
class Juego(models.Model): 
    campo_id = models.ForeignKey('Campo', models.DO_NOTHING, db_column='campo_id', verbose_name="Lugar") 
    fecha_hora = models.DateTimeField()
    equipo_uno = models.ForeignKey('Equipo', models.DO_NOTHING, db_column='equipo_uno', verbose_name="Equipo A")    
    equipo_dos = models.ForeignKey('Equipo', models.DO_NOTHING, db_column='equipo_dos',related_name="equipo_perdedor", verbose_name="Equipo B")  
    carrera_uno = models.IntegerField(verbose_name="Carreras Equipo A")
    carrera_dos = models.IntegerField(verbose_name="Carreras Equipo B")
    error_uno = models.IntegerField(verbose_name="Errores Equipo A")
    error_dos = models.IntegerField(verbose_name="Errores Equipo B")
    hits_uno = models.IntegerField(verbose_name="Hits Equipo A")
    hits_dos = models.IntegerField(verbose_name="Hits Equipo B")
    
    def __str__(self):
        return self.equipo_uno.equipo + "-" + self.equipo_dos.equipo + "(" + self.fecha_hora.strftime("%d-%m-%Y") + ")"
    
    def clean(self, *args, **kwargs):
        uno = self.equipo_uno
        dos = self.equipo_dos
        if uno == dos:
            raise ValidationError('No se puede realizar un juego entre los mismos equipos')
        super().clean(*args, **kwargs)        
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Juego'
        verbose_name_plural = 'Juegos'
        
class Jugador(models.Model):
    TIPO = [
        ("Pitcher", "Pitcher"),
        ("Bateador", "Bateador")
    ]
    
    equipo_id = models.ForeignKey('Equipo', models.DO_NOTHING, db_column='equipo_id', verbose_name="Equipo")
    tipo = models.CharField(max_length=100, choices=TIPO)
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre + "(" + self.equipo_id.equipo + ")" + " - " + self.tipo

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Jugador'
        verbose_name_plural = 'Jugadores'
                
class Pitcheo(models.Model):
    juego_id = models.ForeignKey('Juego', models.DO_NOTHING, db_column='juego_id', verbose_name="Juego")
    jugador_id = models.ForeignKey('Jugador', models.DO_NOTHING, db_column='jugador_id', verbose_name="Pitcher")
    ganado = models.BooleanField(verbose_name="Juego Ganado")
    perdido = models.BooleanField(verbose_name="Juego Perdido")
    sin_decision = models.BooleanField(verbose_name="Juego Sin Decisión")
    hits = models.IntegerField(verbose_name="Hits Permitidos")
    ip = models.IntegerField(verbose_name="IP")
    carreras = models.IntegerField(verbose_name="Carreras permitidas")
    carr_limpias = models.IntegerField(verbose_name="Carreras limpias")
    ponche = models.IntegerField(verbose_name="Ponches")
    bb = models.IntegerField(verbose_name="Base por bolas")
    pcl = models.FloatField(editable=False,null=True, blank=True)
    pcte = models.FloatField(editable=False,null=True, blank=True)
    
    def __str__(self):
        return self.jugador_id.nombre + " en el " + str(self.juego_id)
    
    def clean(self, *args, **kwargs):
        ganado = self.ganado
        perdido = self.perdido
        sin_decision = self.sin_decision
        if ganado and (perdido or sin_decision):
            raise ValidationError('Solo puede ganar, perder o quedar sin decisión')
        if perdido and (ganado or sin_decision):
            raise ValidationError('Solo puede ganar, perder o quedar sin decisión')        
        if sin_decision and (perdido or sin_decision):
            raise ValidationError('Solo puede ganar, perder o quedar sin decisión')
        super().clean(*args, **kwargs)    
    

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Pitcheo'
        verbose_name_plural = 'Pitcheos'
        
class ResumenEquipo(models.Model): 
    equipo = models.ForeignKey('Equipo', models.DO_NOTHING, db_column='equipo_uno', verbose_name="Equipo")
    jugados = models.IntegerField(verbose_name="Juegos Jugados")
    ganados = models.IntegerField(verbose_name="Juegos Ganados")
    perdidos = models.IntegerField(verbose_name="Juegos Perdidos")
    empatados = models.IntegerField(verbose_name="Juegos Empatados")
    pct = models.IntegerField(verbose_name="PCT")
    
    def __str__(self):
        return self.equipo.equipo
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Resumen Equipo'
        verbose_name_plural = 'Resumen Equipos'      
        ordering = ['-ganados']
