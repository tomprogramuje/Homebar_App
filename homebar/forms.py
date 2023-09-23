from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Spirit, Cocktail, Subcategory


class SpiritForm(forms.ModelForm):
    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.all(), required=False)

    class Meta:
        model = Spirit
        fields = ["category", "subcategory", "name", "url"]


class CocktailForm(forms.ModelForm):

    class Meta:
        model = Cocktail
        fields = ["name", "cocktail_category", "base", "ingredients", "recipe"]


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
