# homebar_app

This is the repository for my homebar_app project.

- Built in Python version 3.11
- Uses [Django 4.2.5](https://www.djangoproject.com/)
- Uses [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- Uses [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/)
- Uses [Bootstrap](https://getbootstrap.com/)
- Uses [django-star-ratings](https://pypi.org/project/django-star-ratings/)
- Uses [pytest](https://docs.pytest.org/en/7.4.x/)
- Uses [pytest-django](https://pytest-django.readthedocs.io/en/latest/)

The app as for now can do:
- CRUD Spirits and Cocktails
- view list of all Spirits and Cocktails based on their category and subcategories
- search for spirit and cocktail throughout database
- user registration and authentication
- manage user's individual spirit collections
- manage user's comments to spirits and cocktails
- manage user's ratings to spirits and cocktails
- cocktail suggestions based on spirits in user's collection
- letting user know if they can make a certain cocktail or they are missing the base spirit for it in their collection
- if users don't have a concrete spirit in their collection, app will let them know the starting price point for that bottle and offers a link to that spirit on Heureka.cz
