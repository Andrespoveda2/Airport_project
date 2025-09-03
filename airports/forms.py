from typing import Any
from django import forms


class AirportDistanceForm(forms.Form):
    aeropuerto_origen = forms.CharField(
        max_length=3,
        min_length=3,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Código IATA Origen",
                "pattern": "[A-Z]{3}",
                "title": "Ingrese el código IATA del aeropuerto de origen",
            }
        ),
        label="Código IATA Destino",
    )
    label = "Código IATA Origen"
    aeropuerto_destino = forms.CharField(
        max_length=3,
        min_length=3,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Código IATA Destino Ej: BOG",
                "pattern": "[A-Z]{3}",
                "title": "Ingrese el código IATA del aeropuerto de destino",
            }
        ),
        label="Código IATA Destino",
    )

    def clean_aeropuerto_origen(self):
        codigo = self.cleaned_data["aeropuerto_origen"].strip().upper()
        if not codigo.isalpha():
            raise forms.ValidationError("El código IATA debe contener solo letras.")
        return codigo

    def clean_aeropuerto_destino(self):
        codigo = self.cleaned_data["aeropuerto_destino"].strip().upper()
        if not codigo.isalpha():
            raise forms.ValidationError("El código IATA debe contener solo letras.")
        return codigo
