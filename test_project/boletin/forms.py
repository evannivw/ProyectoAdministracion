from django import forms
class NameForm(forms.Form):
    Valor_minimo = forms.CharField(label='Vmin', max_length=100)