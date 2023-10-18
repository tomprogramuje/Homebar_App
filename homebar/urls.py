from django.urls import path, include
from . import views
from . import url_handler

urlpatterns = [
    path("home", views.HomepageView.as_view(), name="home"),
    path("spirit/<int:pk>/", views.SpiritDetailView.as_view(), name="spirit_detail"),
    path("cocktail/<int:pk>/", views.CocktailDetailView.as_view(), name="cocktail_detail"),
    path("spirit/<int:spirit_id>/comment/create", views.spirit_comment_create, name="spirit_comment_create"),
    path("cocktail/<int:cocktail_id>/comment/create", views.cocktail_comment_create, name="cocktail_comment_create"),
    path("spirit/<int:spirit_id>/comment/<int:comment_id>/delete/", views.spirit_comment_delete, name="spirit_comment_delete"),
    path("cocktail/<int:cocktail_id>/comment/<int:comment_id>/delete/", views.cocktail_comment_delete, name="cocktail_comment_delete"),
    path("spirit/<int:spirit_id>/rating/create", views.spirit_rating_create, name="spirit_rating_create"),
    path("cocktail/<int:cocktail_id>/rating/create", views.cocktail_rating_create, name="cocktail_rating_create"),
    path("spirit/<int:pk>/edit/", views.SpiritEditView.as_view(), name="spirit_edit"),
    path("cocktail/<int:pk>/edit/", views.CocktailEditView.as_view(), name="cocktail_edit"),
    path("spirit/<int:pk>/delete/", views.SpiritDeleteView.as_view(), name="spirit_delete"),
    path("cocktail/<int:pk>/delete/", views.CocktailDeleteView.as_view(), name="cocktail_delete"),
    path("spirit_form/", views.SpiritCreateView.as_view(), name="spirit_form"),
    path("cocktail_form/", views.CocktailCreateView.as_view(), name="cocktail_form"),
    path("spirit_search/", views.spirit_search, name="spirit_search"),
    path("cocktail_search/", views.cocktail_search, name="cocktail_search"),
    path("category/", views.CategoryListView.as_view(), name="category_list"),
    path("cocktail_category/", views.CocktailCategoryListView.as_view(), name="cocktailcategory_list"),
    path("category/<int:category_id>/", views.category_detail, name='category_detail'),
    path("cocktail_category/<int:cocktailcategory_id>/", views.cocktail_category_detail, name='cocktailcategory_detail'),
    path("add_to_collection/<int:spirit_id>/", views.add_to_collection, name="add_to_collection"),
    path("remove_from_collection/<int:spirit_id>/", views.remove_from_collection, name="remove_from_collection"),
    path("remove_from_collection_in_spirit_detail/<int:spirit_id>/", views.remove_from_collection, name="remove_from_collection_in_spirit_detail"),
    path("spirit_collection/", views.view_collection, name="spirit_collection"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path("", url_handler.home_handler),
]
