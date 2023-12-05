# Generated by Django 4.2 on 2023-12-05 01:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Campo',
                'verbose_name_plural': 'Campos',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipo', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Equipo',
                'verbose_name_plural': 'Equipos',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Juego',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField()),
                ('campo_id', models.ForeignKey(db_column='campo_id', on_delete=django.db.models.deletion.DO_NOTHING, to='core.campo')),
                ('equipo_dos', models.ForeignKey(db_column='equipo_dos', on_delete=django.db.models.deletion.DO_NOTHING, related_name='equipo_perdedor', to='core.equipo')),
                ('equipo_uno', models.ForeignKey(db_column='equipo_uno', on_delete=django.db.models.deletion.DO_NOTHING, to='core.equipo')),
            ],
            options={
                'verbose_name': 'Juego',
                'verbose_name_plural': 'Juegos',
                'db_table': 'juego',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('equipo_id', models.ForeignKey(db_column='equipo_id', on_delete=django.db.models.deletion.DO_NOTHING, to='core.equipo')),
            ],
            options={
                'verbose_name': 'Pitcheo',
                'verbose_name_plural': 'Pitcheos',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Pitcheo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jugado', models.IntegerField()),
                ('ganado', models.IntegerField()),
                ('perdido', models.IntegerField()),
                ('sin_decision', models.IntegerField()),
                ('veces', models.IntegerField()),
                ('hits', models.IntegerField()),
                ('ip', models.IntegerField()),
                ('carreras', models.IntegerField()),
                ('carr_limpias', models.IntegerField()),
                ('ponche', models.IntegerField()),
                ('bb', models.IntegerField()),
                ('pcl', models.FloatField()),
                ('pcte', models.FloatField()),
                ('juego_id', models.ForeignKey(db_column='juego_id', on_delete=django.db.models.deletion.DO_NOTHING, to='core.juego')),
                ('jugador_id', models.ForeignKey(db_column='jugador_id', on_delete=django.db.models.deletion.DO_NOTHING, to='core.jugador')),
            ],
            options={
                'verbose_name': 'Pitcheo',
                'verbose_name_plural': 'Pitcheos',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Liga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('titulo_uno', models.CharField(max_length=200)),
                ('titulo_dos', models.CharField(max_length=200)),
                ('periodo', models.CharField(max_length=200)),
                ('logo', models.ImageField(upload_to='')),
                ('anno', models.IntegerField()),
                ('responsable', models.CharField(max_length=100)),
                ('categoria_id', models.ForeignKey(db_column='categoria_id', on_delete=django.db.models.deletion.DO_NOTHING, to='core.categoria')),
                ('temporada_id', models.ForeignKey(db_column='temporada_id', on_delete=django.db.models.deletion.DO_NOTHING, to='core.temporada')),
            ],
            options={
                'verbose_name': 'Liga',
                'verbose_name_plural': 'Ligas',
                'db_table': 'liga',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('liga_id', models.ForeignKey(db_column='liga_id', on_delete=django.db.models.deletion.DO_NOTHING, to='core.liga')),
            ],
            options={
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='equipo',
            name='grupo_id',
            field=models.ForeignKey(db_column='grupo_id', on_delete=django.db.models.deletion.DO_NOTHING, to='core.grupo'),
        ),
        migrations.CreateModel(
            name='Bateo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('veces_bate', models.IntegerField()),
                ('hits', models.IntegerField()),
                ('doble', models.IntegerField()),
                ('triple', models.IntegerField()),
                ('home_run', models.IntegerField()),
                ('carrera', models.IntegerField()),
                ('base_robada', models.IntegerField()),
                ('base_bola', models.IntegerField()),
                ('ponche', models.IntegerField()),
                ('juego_id', models.ForeignKey(db_column='juego_id', on_delete=django.db.models.deletion.DO_NOTHING, to='core.juego')),
                ('jugador_id', models.ForeignKey(db_column='jugador_id', on_delete=django.db.models.deletion.DO_NOTHING, to='core.jugador')),
            ],
            options={
                'verbose_name': 'Bateo',
                'verbose_name_plural': 'Bateos',
                'db_table': '',
                'managed': True,
            },
        ),
    ]