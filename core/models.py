from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey, GroupedForeignKey

class Campeonato(models.Model):
    liga_id = models.ForeignKey('Liga', models.DO_NOTHING, db_column='liga_id', verbose_name="Liga")
    nombre = models.CharField(max_length=50) 
    
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Campeonato'
        verbose_name_plural = 'Campeonato'
        
class Bateo(models.Model):
    liga_id = models.ForeignKey('Liga', models.DO_NOTHING, db_column='liga_id', verbose_name="Liga")
    campeonato = ChainedForeignKey(
        "Campeonato",
        related_name = "camb_id",
        chained_field="liga_id",
        chained_model_field="liga_id",
        verbose_name="Campeonato",
        show_all=False,
        auto_choose=True,
        sort=True)
    categoria = ChainedForeignKey(
        "Categoria",
        related_name = "catb_id",
        chained_field="campeonato",
        chained_model_field="campeonato",
        verbose_name="Categoria",
        show_all=False,
        auto_choose=True,
        sort=True)
    grupo = ChainedForeignKey(
        "Grupo",
        related_name = "gpbat_id",
        verbose_name="Grupo",
        chained_field="categoria",
        chained_model_field="categoria",
        show_all=False,
        auto_choose=True,
        sort=True)
    juego = ChainedForeignKey(
        "Juego",
        related_name = "jue_id",
        verbose_name="Juego",
        chained_field="grupo",
        chained_model_field="grupo",
        show_all=False,
        auto_choose=True,
        sort=True)
    equipo = ChainedForeignKey(
        "Equipo",
        related_name = "equip_id",
        verbose_name="Equipo",
        chained_field="categoria",
        chained_model_field="categoria",
        show_all=False,
        auto_choose=True,
        sort=True)
    jugador_id = ChainedForeignKey(
        "Jugador",
        related_name = "jugador_id",
        verbose_name="Jugador",
        chained_field="equipo",
        chained_model_field="equipo",
        show_all=False,
        auto_choose=True,
        sort=True)
    veces_bate = models.IntegerField(verbose_name="Veces al Bate", default=0)
    hits = models.IntegerField(verbose_name="Hits", default=0)
    doble = models.IntegerField(verbose_name="Dobles", default=0)
    triple = models.IntegerField(verbose_name="Triples", default=0)
    home_run = models.IntegerField(verbose_name="Home Run", default=0)
    carrera = models.IntegerField(verbose_name="Carreras producidas", default=0)
    base_robada = models.IntegerField(verbose_name="Bases robadas", default=0)
    base_bola = models.IntegerField(verbose_name="Bases por bolas", default=0)
    ponche = models.IntegerField(verbose_name="Ponches", default=0)
    
    def __str__(self):
        return self.jugador_id.nombre + " en el " + str(self.juego) + " de " + self.liga_id.nombre

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
                
class Categoria(models.Model):
    liga_id = models.ForeignKey('Liga', models.DO_NOTHING, db_column='liga_id', verbose_name="Liga")
    campeonato = ChainedForeignKey(
        "Campeonato",
        related_name = "campeonato_id",
        chained_field="liga_id", 
        verbose_name="Campeonato",
        chained_model_field="liga_id",
        show_all=False,
        auto_choose=True,
        sort=True)
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        
class Liga(models.Model):
    nombre = models.CharField(max_length=200)
    titulo_uno = models.CharField(max_length=200, verbose_name="Título del Torneo")
    periodo = models.CharField(max_length=200, verbose_name="Período")
    logo = models.ImageField()
    anno = models.IntegerField(verbose_name="Año")
    responsable = models.CharField(max_length=100, verbose_name="Responsable")    
    
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Liga'
        verbose_name_plural = 'Ligas'
        
class Grupo(models.Model):
    liga_id = models.ForeignKey('Liga', models.DO_NOTHING, db_column='liga_id', verbose_name="Liga")
    campeonato = ChainedForeignKey(
        "Campeonato",
        related_name = "campeonat_id",
        chained_field="liga_id",
        chained_model_field="liga_id",
        verbose_name="Campeonato",
        show_all=False,
        auto_choose=True,
        sort=True)
    categoria = ChainedForeignKey(
        "Categoria",
        related_name = "categoria_id",
        chained_field="campeonato",
        chained_model_field="campeonato",
        verbose_name="Categoria",
        show_all=False,
        auto_choose=True,
        sort=True)
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'

class Equipo(models.Model):
    liga_id = models.ForeignKey('Liga', models.DO_NOTHING, db_column='liga_id', verbose_name="Liga")
    campeonato = ChainedForeignKey(
        "Campeonato",
        related_name = "campeon_id",
        chained_field="liga_id",
        chained_model_field="liga_id",
        show_all=False,
        verbose_name="Campeonato",
        auto_choose=True,
        sort=True)
    categoria = ChainedForeignKey(
        "Categoria",
        related_name = "categor_id",
        chained_field="campeonato",
        chained_model_field="campeonato",
        verbose_name="Categoria",
        show_all=False,
        auto_choose=True,
        sort=True)
    grupo = ChainedForeignKey(
        "Grupo",
        related_name = "grupo_id",
        chained_field="categoria",
        chained_model_field="categoria",
        verbose_name="Grupo",
        show_all=False,
        auto_choose=True,
        sort=True)
    equipo = models.CharField(max_length=200)
    
    def __str__(self):
        return self.equipo

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        
class Juego(models.Model):
    fecha_hora = models.DateTimeField()    
    liga_id = models.ForeignKey('Liga', models.DO_NOTHING, db_column='liga_id', verbose_name="Liga")
    campeonato = ChainedForeignKey(
        "Campeonato",
        related_name = "cam_id",
        chained_field="liga_id",
        chained_model_field="liga_id",
        show_all=False,
        verbose_name="Campeonato",
        auto_choose=True,
        sort=True)
    categoria = ChainedForeignKey(
        "Categoria",
        related_name = "cat_id",
        chained_field="campeonato",
        chained_model_field="campeonato",
        show_all=False,
        verbose_name="Categoria",
        auto_choose=True,
        sort=True)
    grupo = ChainedForeignKey(
        "Grupo",
        related_name = "gp_id",
        verbose_name="Grupo Equipo A",
        chained_field="categoria",
        chained_model_field="categoria",
        show_all=False,
        auto_choose=True,
        sort=True)
    equipo_uno = ChainedForeignKey(
        "Equipo",
        related_name = "equipo_uno_id",
        verbose_name="Equipo A",
        chained_field="grupo",
        chained_model_field="grupo",
        show_all=False,
        auto_choose=True,
        sort=True)   
    grupob = ChainedForeignKey(
        "Grupo",
        related_name = "gpb_id",
        verbose_name="Grupo Equipo B",
        chained_field="categoria",
        chained_model_field="categoria",
        show_all=False,
        auto_choose=True,
        sort=True)
    equipo_dos = ChainedForeignKey(
        "Equipo",
        related_name = "equipo_dos_id",
        verbose_name="Equipo B",
        chained_field="grupob",
        chained_model_field="grupo",
        show_all=False,
        auto_choose=True,
        sort=True)
    carrera_uno = models.IntegerField(verbose_name="Carreras Equipo A", default=0)
    carrera_dos = models.IntegerField(verbose_name="Carreras Equipo B", default=0)
    error_uno = models.IntegerField(verbose_name="Errores Equipo A", default=0)
    error_dos = models.IntegerField(verbose_name="Errores Equipo B", default=0)
    hits_uno = models.IntegerField(verbose_name="Hits Equipo A", default=0)
    hits_dos = models.IntegerField(verbose_name="Hits Equipo B", default=0)
    finalizado = models.BooleanField(verbose_name="Terminado")
    
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
    
    liga_id = models.ForeignKey('Liga', models.DO_NOTHING, db_column='liga_id', verbose_name="Liga")
    campeonato = ChainedForeignKey(
        "Campeonato",
        related_name = "camp_id",
        chained_field="liga_id",
        verbose_name="Campeonato",
        chained_model_field="liga_id",
        show_all=False,
        auto_choose=True,
        sort=True)
    categoria = ChainedForeignKey(
        "Categoria",
        related_name = "categ_id",
        chained_field="campeonato",
        chained_model_field="campeonato",
        verbose_name="Categoria",
        show_all=False,
        auto_choose=True,
        sort=True)
    grupo = ChainedForeignKey(
        "Grupo",
        related_name = "grup_id",
        chained_field="categoria",
        chained_model_field="categoria",
        verbose_name="Grupo",
        show_all=False,
        auto_choose=True,
        sort=True)
    equipo = ChainedForeignKey(
        "Equipo",
        related_name = "equipo_id",
        chained_field="grupo",
        chained_model_field="grupo",
        verbose_name="Equipo",
        show_all=False,
        auto_choose=True,
        sort=True)
    tipo = models.CharField(max_length=100, choices=TIPO)
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre + "(" + self.equipo.equipo + ")" + " - " + self.tipo

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Jugador'
        verbose_name_plural = 'Jugadores'
                
class Pitcheo(models.Model):
    liga_id = models.ForeignKey('Liga', models.DO_NOTHING, db_column='liga_id', verbose_name="Liga")
    campeonato = ChainedForeignKey(
        "Campeonato",
        related_name = "cambp_id",
        verbose_name="Campeonato",
        chained_field="liga_id",
        chained_model_field="liga_id",
        show_all=False,
        auto_choose=True,
        sort=True)
    categoria = ChainedForeignKey(
        "Categoria",
        related_name = "catbp_id",
        chained_field="campeonato",
        chained_model_field="campeonato",
        verbose_name="Categoria",
        show_all=False,
        auto_choose=True,
        sort=True)
    grupo = ChainedForeignKey(
        "Grupo",
        related_name = "gpbatp_id",
        verbose_name="Grupo",
        chained_field="categoria",
        chained_model_field="categoria",
        show_all=False,
        auto_choose=True,
        sort=True)
    juego = ChainedForeignKey(
        "Juego",
        related_name = "juep_id",
        verbose_name="Juego",
        chained_field="grupo",
        chained_model_field="grupo",
        show_all=False,
        auto_choose=True,
        sort=True)
    equipo = ChainedForeignKey(
        "Equipo",
        related_name = "equipp_id",
        verbose_name="Equipo",
        chained_field="categoria",
        chained_model_field="categoria",
        show_all=False,
        auto_choose=True,
        sort=True)
    jugador_id = ChainedForeignKey(
        "Jugador",
        related_name = "jugadorp_id",
        verbose_name="Jugador",
        chained_field="equipo",
        chained_model_field="equipo",
        show_all=False,
        auto_choose=True,
        sort=True)
    ganado = models.BooleanField(verbose_name="Juego Ganado")
    perdido = models.BooleanField(verbose_name="Juego Perdido")
    sin_decision = models.BooleanField(verbose_name="Juego Sin Decisión")
    hits = models.IntegerField(verbose_name="Hits Permitidos", default=0)
    ip = models.IntegerField(verbose_name="IP", default=0)
    carreras = models.IntegerField(verbose_name="Carreras permitidas", default=0)
    carr_limpias = models.IntegerField(verbose_name="Carreras limpias", default=0)
    ponche = models.IntegerField(verbose_name="Ponches", default=0)
    bb = models.IntegerField(verbose_name="Base por bolas", default=0)
    pcl = models.FloatField(editable=False,null=True, blank=True, default=0)
    pcte = models.FloatField(editable=False,null=True, blank=True, default=0)
    
    def __str__(self):
        return self.jugador_id.nombre + " en el " + str(self.juego) + " de " + self.liga_id.nombre
    
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
    liga_id = models.ForeignKey('Liga', models.DO_NOTHING, db_column='liga_id', verbose_name="Liga")
    campeonato = ChainedForeignKey(
        "Campeonato",
        related_name = "campc_id",
        chained_field="liga_id",
        chained_model_field="liga_id",
        verbose_name="Campeonato",
        show_all=False,
        auto_choose=True,
        sort=True)
    categoria = ChainedForeignKey(
        "Categoria",
        related_name = "categc_id",
        chained_field="campeonato",
        chained_model_field="campeonato",
        verbose_name="Categoria",
        show_all=False,
        auto_choose=True,
        sort=True)
    grupo = ChainedForeignKey(
        "Grupo",
        related_name = "grupc_id",
        chained_field="categoria",
        chained_model_field="categoria",
        verbose_name="Grupo",
        show_all=False,
        auto_choose=True,
        sort=True)
    equipo = ChainedForeignKey(
        "Equipo",
        related_name = "equipoc_id",
        chained_field="grupo",
        chained_model_field="grupo",
        verbose_name="Equipo",
        show_all=False,
        auto_choose=True,
        sort=True)
    jugados = models.IntegerField(verbose_name="Juegos Jugados", default=0)
    ganados = models.IntegerField(verbose_name="Juegos Ganados", default=0)
    perdidos = models.IntegerField(verbose_name="Juegos Perdidos", default=0)
    empatados = models.IntegerField(verbose_name="Juegos Empatados", default=0)
    pct = models.IntegerField(verbose_name="PCT", default=0)
    
    def __str__(self):
        return self.equipo.equipo + " - " + str(self.grupo) + " - " + self.liga_id.nombre
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Resumen Equipo'
        verbose_name_plural = 'Resumen Equipos'      
        ordering = ['-ganados']
