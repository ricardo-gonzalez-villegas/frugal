from multiprocessing import context
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .helper.search import SearchThread
from .helper.favorite import favorite_products
from .models import Favorite, Product


def welcome_view(request):
    return render(request, "frugal/welcome.html")


def registration_view(request):
    return HttpResponse("Registration Index")


def login_view(request):
    # if user is logged in redirects to home view
    if request.user.is_authenticated:
        return home_view(request)
    else:
        # login user
        if request.POST:
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            # if successful redirects to index view
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("home"))
            else:
                return HttpResponse("Error")
        else:
            # if user is not logged in redirects to login page
            return render(request, "frugal/login.html")


@login_required(redirect_field_name="")
def logout_view(request):
    logout(request)
    return render(request, "frugal/login.html")


@login_required(redirect_field_name="")
def home_view(request):
    return render(request, "frugal/home.html")


@login_required(redirect_field_name="")
def search_view(request):
    return render(request, "frugal/search.html")


@login_required(redirect_field_name="")
def results_view(request):
    if request.GET:
        search = SearchThread(request)
        context = {
            "title": f'Search Results for {request.GET["search"].capitalize()}',
            "results": search.get_results(),
        }
    return render(request, "frugal/results.html", context)


@login_required(redirect_field_name="")
def favorite_view(request):
    if request.POST:
        favorite = favorite_products(request)
        return HttpResponseRedirect(reverse("details", args=(favorite.pk,)))


@login_required(redirect_field_name="")
def favorites_view(request):
    user_favorites = Favorite.objects.filter(user_id=request.user.id)
    context = {"user_favorites": user_favorites}
    return render(request, "frugal/favorites.html", context)


@login_required(redirect_field_name="")
def favorite_details(request, favorite_id):
    user_favorite = Favorite.objects.get(pk=favorite_id)
    user_favorited_products = Product.objects.filter(favorite_id=favorite_id)
    context = {
        "user_favorite": user_favorite,
        "user_favorited_products": user_favorited_products,
    }
    return render(request, "frugal/details.html", context)
