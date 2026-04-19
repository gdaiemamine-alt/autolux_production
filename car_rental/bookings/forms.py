from django import forms
from .models import Booking
from django.utils import timezone

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'pickup_location', 'return_location', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pickup_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lieu de prise en charge'}),
            'return_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lieu de retour'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Remarques supplémentaires...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        today = timezone.now().date()

        if start_date and start_date < today:
            raise forms.ValidationError("La date de début ne peut pas être dans le passé.")
        if start_date and end_date and end_date <= start_date:
            raise forms.ValidationError("La date de fin doit être après la date de début.")
        return cleaned_data
