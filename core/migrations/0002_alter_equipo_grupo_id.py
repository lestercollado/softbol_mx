# Generated by Django 4.2 on 2023-12-06 20:23

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipo',
            name='grupo_id',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='liga_id', chained_model_field='liga_id', on_delete=django.db.models.deletion.CASCADE, to='core.grupo'),
        ),
    ]
