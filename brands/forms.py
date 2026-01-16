from django import forms


class BrandForm(forms.Form):
    SAVE_CHOICES = [
        ("file_json", "В файл JSON"),
        ("file_xml", "В файл XML"),
        ("db", "В базу данных (SQLite)"),
    ]

    name = forms.CharField(
        max_length=100,
        label="Название марки",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    country = forms.CharField(
        max_length=100,
        label="Страна",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    founded = forms.IntegerField(
        label="Год основания",
        min_value=1800,
        max_value=2100,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    description = forms.CharField(
        label="Описание",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4})
    )

    save_to = forms.ChoiceField(
        choices=SAVE_CHOICES,
        label="Куда сохранить",
        widget=forms.Select(attrs={"class": "form-select"})
    )
