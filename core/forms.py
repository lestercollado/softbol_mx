from django import forms
from .models import Campeonato, Liga, Categoria
from smart_selects.form_fields import ChainedModelChoiceField

class ReporteEstadoActualForm(forms.Form):
    liga = forms.ModelChoiceField(queryset=Liga.objects.all(),
        widget=forms.Select(
        attrs={'class': "form-control"}))
    campeonato = ChainedModelChoiceField(        
        queryset=Campeonato.objects.all(),
        empty_label='Seleccionar...',
        label='Campeonato',
        to_app_name='core', to_model_name='Campeonato', chained_field='liga', chained_model_field='liga_id',
        foreign_key_app_name='core', foreign_key_model_name='Categoria', foreign_key_field_name='campeonato',
        show_all=False, auto_choose=True
    )
    categoria = ChainedModelChoiceField(        
        queryset=Categoria.objects.all(),
        empty_label='Seleccionar...',
        label='Categoria',
        to_app_name='core', to_model_name='Categoria', chained_field='campeonato', chained_model_field='campeonato',
        foreign_key_app_name='core', foreign_key_model_name='Categoria', foreign_key_field_name='categoria',
        show_all=False, auto_choose=True
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        self.fields['campeonato'].widget.attrs['class'] = 'chained-fk form-control'
        self.fields['categoria'].widget.attrs['class'] = 'chained-fk form-control'
        
class BateoGeneralForm(forms.Form):
    liga = forms.ModelChoiceField(queryset=Liga.objects.all(),
        widget=forms.Select(
        attrs={'class': "form-control"}))
    campeonato = ChainedModelChoiceField(        
        queryset=Campeonato.objects.all(),
        empty_label='Seleccionar...',
        label='Campeonato',
        to_app_name='core', to_model_name='Campeonato', chained_field='liga', chained_model_field='liga_id',
        foreign_key_app_name='core', foreign_key_model_name='Categoria', foreign_key_field_name='campeonato',
        show_all=False, auto_choose=True
    )
    categoria = ChainedModelChoiceField(        
        queryset=Categoria.objects.all(),
        empty_label='Seleccionar...',
        label='Categoria',
        to_app_name='core', to_model_name='Categoria', chained_field='campeonato', chained_model_field='campeonato',
        foreign_key_app_name='core', foreign_key_model_name='Categoria', foreign_key_field_name='categoria',
        show_all=False, auto_choose=True
    )
    veces = forms.IntegerField(label="Veces Legales")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        self.fields['campeonato'].widget.attrs['class'] = 'chained-fk form-control'
        self.fields['categoria'].widget.attrs['class'] = 'chained-fk form-control'
        self.fields['veces'].widget.attrs['class'] = 'form-control'