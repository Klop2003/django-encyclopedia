from django import forms

SAVE_TO_CHOICES = [
    ("db", "В базу данных (SQLite)"),
    ("file_json", "В файл JSON"),
    ("file_xml", "В файл XML"),
]

class BrandForm(forms.Form):
    name = forms.CharField(
        max_length=100, label="Название марки",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    country = forms.CharField(
        max_length=100, label="Страна",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    founded = forms.IntegerField(
        label="Год основания", min_value=1800, max_value=2100,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        label="Описание"
    )
    save_to = forms.ChoiceField(
        choices=SAVE_TO_CHOICES,
        label="Куда сохранить",
        widget=forms.Select(attrs={"class": "form-select"})
    )
