from django import forms

class BrandForm(forms.Form):
    name = forms.CharField(max_length=100, label="Название марки")
    country = forms.CharField(max_length=100, label="Страна")
    founded = forms.IntegerField(label="Год основания", min_value=1800, max_value=2100)
    description = forms.CharField(widget=forms.Textarea, label="Описание")
