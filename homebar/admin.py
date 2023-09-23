from django.contrib import admin
from .models import Spirit, UserCollection, SpiritComment, CocktailComment, Comment, Category, Subcategory, Cocktail, CocktailCategory

# Register your models here.

admin.site.register(Spirit)
admin.site.register(UserCollection)
admin.site.register(SpiritComment)
admin.site.register(CocktailComment)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Cocktail)
admin.site.register(CocktailCategory)
