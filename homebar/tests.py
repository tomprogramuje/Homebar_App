from django.utils import timezone
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch, Mock
import pytest
from .models import Spirit, Category, Subcategory, CocktailCategory
from .forms import SpiritForm, CocktailForm, RegistrationForm

# Create your tests here.


@pytest.mark.django_db
def test_fetch_price():
    gin_category = Category.objects.create(name="Gin")
    old_tom_subcategory = Subcategory.objects.create(name="Old Tom", base_spirit=gin_category)

    spirit = Spirit(
        category=gin_category,
        subcategory=old_tom_subcategory,
        name="Test Spirit",
        price=None,
        url="http://example.com",
        pub_date=timezone.now(),
    )

    mock_response = Mock()
    mock_response.text = '<title>Cena od 100 Kč</title>'

    with patch('requests.get', return_value=mock_response):
        spirit.fetch_price()

    assert spirit.price == "100"


@pytest.mark.django_db
def test_spirit_form():
    client = Client()
    vodka_category = Category.objects.create(name="Vodka")
    subcategory = Subcategory.objects.create(name="Test Subcategory", base_spirit=vodka_category)
    form_data = {
        "category": vodka_category.id,
        "subcategory": subcategory.id,
        "name": "Test Spirit",
        "url": "http://example.com",
    }

    response = client.post(reverse("spirit_form"), data=form_data)
    assert response.status_code == 302

    form = SpiritForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_cocktail_form():
    client = Client()
    vodka_category = Category.objects.create(name="Vodka")
    subcategory = Subcategory.objects.create(name="Test Subcategory", base_spirit=vodka_category)
    vodka_cocktail_category = CocktailCategory.objects.create(name="Vodka Cocktails")
    form_data = {
        "name": "Vodka Cranberry",
        "cocktail_category": vodka_cocktail_category,
        "base": subcategory.id,
        "ingredients": "Cranberry juice",
        "recipe": "Test Recipe",
    }

    response = client.post(reverse("cocktail_form"), data=form_data)
    assert response.status_code == 302

    form = CocktailForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_registration_form():
    client = Client()

    form_data = {
        "username": "TestUser",
        "email": "invalid_email",
        "password1": "regularuser",
        "password2": "regularuser",
    }

    response = client.post(reverse("sign_up"), data=form_data, follow=True)
    assert response.status_code == 200

    form = RegistrationForm(data=form_data)
    assert not User.objects.filter(username="TestUser").exists()
