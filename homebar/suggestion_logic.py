from random import choice
from .models import Cocktail, UserCollection


def suggest_cocktail(user):
    user_spirit_categories = UserCollection.objects.filter(user=user).values_list('spirit__subcategory', flat=True)
    candidate_cocktails = Cocktail.objects.filter(base__in=user_spirit_categories)
    if candidate_cocktails.exists():
        return choice(candidate_cocktails)
    return None
