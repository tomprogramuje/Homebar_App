from django.contrib.auth.models import User
from django.db import models
from star_ratings.models import Rating as StarRating
import requests
import re
from bs4 import BeautifulSoup

# Create your models here.


class Rating(models.Model):
    star_rating = models.OneToOneField(StarRating, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.star_rating.rating)


class Comment(models.Model):
    text = models.TextField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Category(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    base_spirit = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = "Subcategories"

    def __str__(self):
        return self.name


class Spirit(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    price = models.IntegerField(blank=True, null=True)
    url = models.URLField(max_length=200, blank=True, null=True)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.name

    def fetch_price(self):
        if self.url:
            try:
                result = requests.get(self.url)
                doc = BeautifulSoup(result.text, "html.parser")
                tag = doc.find("title")
                price_text = tag.string

                match = re.search(r'\bod\b', price_text)

                if match:
                    start_index = match.end()
                    end_index = price_text.find("Kč", start_index)

                    if end_index >= 0:
                        self.price = price_text[start_index:end_index].strip()
            except Exception as e:
                pass


class CocktailCategory(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name = "Cocktail Category"
        verbose_name_plural = "Cocktail Categories"

    def __str__(self):
        return self.name


class Cocktail(models.Model):
    name = models.CharField(max_length=25)
    cocktail_category = models.ForeignKey(CocktailCategory, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("date published")
    base = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    ingredients = models.TextField(max_length=300)
    recipe = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class SpiritComment(models.Model):
    spirit = models.ForeignKey(Spirit, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("spirit", "comment")


class CocktailComment(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("cocktail", "comment")


class SpiritRating(models.Model):
    spirit = models.ForeignKey(Spirit, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("spirit", "rating")


class CocktailRating(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("cocktail", "rating")


class UserCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spirit = models.ForeignKey(Spirit, on_delete=models.CASCADE)
    ratings = models.ManyToManyField(Rating)
    comments = models.ManyToManyField(Comment)
