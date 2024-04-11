from django import forms
from adminapp.models import dishes

class DishForm(forms.ModelForm):
    class Meta:
        model = dishes
        fields = '__all__'
