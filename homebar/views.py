from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Spirit, UserCollection, Comment, SpiritComment, SpiritRating, Rating, Cocktail, CocktailComment, \
    Category, CocktailRating, CocktailCategory
from star_ratings.models import Rating as StarRating
import requests
from bs4 import BeautifulSoup
from .forms import SpiritForm, RegistrationForm, CocktailForm
from .suggestion_logic import suggest_cocktail


# Create your views here.


class SpiritDetailView(generic.DetailView):

    model = Spirit
    template_name = "homebar/spirit_detail.html"
    context_object_name = "spirit"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        spirit = context['spirit']
        comments = SpiritComment.objects.filter(spirit=spirit)
        category = self.object.category
        subcategory = self.object.subcategory

        if user.is_authenticated:
            user_has_spirit_in_collection = UserCollection.objects.filter(user=user, spirit=spirit).exists()
        else:
            user_has_spirit_in_collection = False

        context['user_has_spirit_in_collection'] = user_has_spirit_in_collection
        context['spiritcomment'] = comments
        context['category'] = category
        context['subcategory'] = subcategory
        spirit.fetch_price()
        context['price'] = spirit.price
        return context


class SpiritCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.CreateView):

    form_class = SpiritForm
    template_name = "homebar/spirit_form.html"
    permission_required = "homebar.add_choice"

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            spirit = form.save(commit=False)
            spirit.pub_date = timezone.now()
            spirit.save()
        return redirect(reverse("category_list"))


class SpiritEditView(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.UpdateView):

    model = Spirit
    fields = ["category", "name"]
    template_name_suffix = "_edit_form"
    permission_required = "homebar.change_choice"

    def get_success_url(self):
        return reverse("spirit_detail", kwargs={"pk": self.object.pk})


class SpiritDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.DeleteView):

    model = Spirit
    success_url = reverse_lazy("category_list")
    permission_required = "homebar.delete_choice"


class CocktailDetailView(generic.DetailView):
    model = Cocktail
    template_name = "homebar/cocktail_detail.html"
    context_object_name = "cocktail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cocktail = context['cocktail']
        comments = CocktailComment.objects.filter(cocktail=cocktail)

        if self.request.user.is_authenticated:
            user = self.request.user
            spirit_in_user_collection = UserCollection.objects.filter(user=user).values_list('spirit__subcategory', flat=True)
        else:
            spirit_in_user_collection = []

        context['cocktail_category'] = self.object.cocktail_category
        context['cocktailcomment'] = comments
        context['spirit_in_user_collection'] = spirit_in_user_collection
        return context


class CocktailCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.CreateView):

    form_class = CocktailForm
    template_name = "homebar/cocktail_form.html"
    permission_required = "homebar.add_choice"

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cocktail = form.save(commit=False)
            cocktail.pub_date = timezone.now()
            cocktail.save()
        return redirect(reverse("cocktailcategory_list"))


class CocktailEditView(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.UpdateView):

    model = Cocktail
    fields = ["name", "base", "ingredients"]
    template_name_suffix = "_edit_form"
    permission_required = "homebar.change_choice"

    def get_success_url(self):
        return reverse("cocktail_detail", kwargs={"pk": self.object.pk})


class CocktailDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.DeleteView):

    model = Cocktail
    success_url = reverse_lazy("cocktailcategory_list")
    permission_required = "homebar.delete_choice"


def spirit_search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        spirits = Spirit.objects.filter(name__contains=searched)
        return render(request, "homebar/spirit_search.html", {"searched": searched, "spirits": spirits})
    return render(request, "homebar/spirit_search.html", {})


def cocktail_search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        cocktails = Cocktail.objects.filter(name__contains=searched)
        return render(request, "homebar/cocktail_search.html", {"searched": searched, "cocktails": cocktails})
    return render(request, "homebar/cocktail_search.html", {})


class CategoryListView(generic.ListView):

    queryset = Category.objects.all()
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spirit_list = Spirit.objects.order_by("-pub_date")[:5]
        context["spirit_list"] = spirit_list
        return context


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    spirits_in_category = Spirit.objects.filter(category=category)
    return render(request, 'homebar/category_detail.html', {'category': category, 'spirits_in_category': spirits_in_category})


@login_required(login_url="/login")
def add_to_collection(request, spirit_id):
    if request.method == "GET":
        spirit = Spirit.objects.get(id=spirit_id)
        user = request.user
        if not UserCollection.objects.filter(user=user, spirit=spirit).exists():
            UserCollection.objects.create(user=user, spirit=spirit)
        else:
            messages.info(request, "You already have this spirit in your collection!")
    spirit_detail_url = reverse('spirit_detail', args=[spirit_id])
    return redirect(spirit_detail_url)


@login_required(login_url="/login")
def remove_from_collection(request, spirit_id):
    if request.method == "POST":
        spirit = Spirit.objects.get(id=spirit_id)
        user = request.user
        try:
            collection_entry = UserCollection.objects.get(user=user, spirit=spirit)
            collection_entry.delete()
        except UserCollection.DoesNotExist:
            messages.info(request, "You don't have this spirit in your collection!")
    spirit_detail_url = reverse('spirit_detail', args=[spirit_id])
    return redirect(spirit_detail_url)


@login_required(login_url="/login")
def remove_from_collection_in_spirit_detail(request, spirit_id):
    if request.method == "POST":
        spirit = Spirit.objects.get(id=spirit_id)
        user = request.user
        try:
            collection_entry = UserCollection.objects.get(user=user, spirit=spirit)
            collection_entry.delete()
        except UserCollection.DoesNotExist:
            messages.info(request, "You don't have this spirit in your collection!")
    collection = UserCollection.objects.filter(user=request.user)
    return render(request, "homebar/spirit_detail.html", {"spirit": spirit})


@login_required(login_url="/login")
def view_collection(request):
    if request.method == "GET":
        collection = UserCollection.objects.filter(user=request.user)
        suggested_cocktail = suggest_cocktail(request.user)
        return render(request, "homebar/spirit_collection.html", {"collection": collection, "suggested_cocktail": suggested_cocktail})


def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/homebar/home")
    else:
        form = RegistrationForm()
    return render(request, "registration/sign_up.html", {"form": form})


@login_required(login_url="/login")
def spirit_comment_create(request, spirit_id):
    spirit = get_object_or_404(Spirit, id=spirit_id)
    if request.method == "POST":
        commented = request.POST["commented"]
        if commented:
            comment = Comment.objects.create(text=commented, author=request.user)
            SpiritComment.objects.create(spirit=spirit, comment=comment)

    return redirect("spirit_detail", pk=spirit_id)


@login_required(login_url="/login")
def spirit_comment_delete(request, spirit_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        if request.user.is_superuser or comment.author.username == request.user.username:
            comment.delete()

    return redirect("spirit_detail", pk=spirit_id)


@login_required(login_url="/login")
def spirit_rating_create(request, spirit_id):
    spirit = get_object_or_404(Spirit, id=spirit_id)
    if request.method == "POST":
        rated = request.POST.get("rating")
        if rated:
            star_rating = StarRating.objects.create(rating=rated)
            user_rating = Rating.objects.create(star_rating=star_rating, author=request.user)
            SpiritRating.objects.create(spirit=spirit, rating=user_rating)

    return redirect("spirit_detail", pk=spirit_id)


@login_required(login_url="/login")
def cocktail_comment_create(request, cocktail_id):
    cocktail = get_object_or_404(Cocktail, id=cocktail_id)
    if request.method == "POST":
        commented = request.POST["commented"]
        if commented:
            comment = Comment.objects.create(text=commented, author=request.user)
            CocktailComment.objects.create(cocktail=cocktail, comment=comment)

    return redirect("cocktail_detail", pk=cocktail_id)


@login_required(login_url="/login")
def cocktail_comment_delete(request, cocktail_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        if request.user.is_superuser or comment.author.username == request.user.username:
            comment.delete()

    return redirect("cocktail_detail", pk=cocktail_id)


@login_required(login_url="/login")
def cocktail_rating_create(request, cocktail_id):
    spirit = get_object_or_404(Cocktail, id=cocktail_id)
    if request.method == "POST":
        rated = request.POST.get("rating")
        if rated:
            star_rating = StarRating.objects.create(rating=rated)
            user_rating = Rating.objects.create(star_rating=star_rating, author=request.user)
            CocktailRating.objects.create(spirit=spirit, rating=user_rating)

    return redirect("spirit_detail", pk=cocktail_id)


class CocktailCategoryListView(generic.ListView):
    queryset = CocktailCategory.objects.all()
    context_object_name = "cocktailcategory"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cocktail_list = Cocktail.objects.order_by("-pub_date")[:5]
        context['cocktail_list'] = cocktail_list
        return context


def cocktail_category_detail(request, cocktailcategory_id):
    cocktail_category = get_object_or_404(CocktailCategory, id=cocktailcategory_id)
    cocktails_in_category = Cocktail.objects.filter(cocktail_category=cocktail_category)
    return render(request, 'homebar/cocktailcategory_detail.html', {'cocktail_category': cocktail_category, 'cocktails_in_category': cocktails_in_category})


class HomepageView(generic.TemplateView):
    template_name = "homebar/home.html"
