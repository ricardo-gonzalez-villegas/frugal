from re import search
from urllib import request
from webbrowser import get
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .helper.search import SearchThread
from .helper.model_helpers import save_to_favorite_and_products, update_product_prices
from .models import Favorite, Product
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.http import JsonResponse


def welcome_view(request):
    return render(request, "frugal/welcome.html")


def registration_view(request):
    if request.POST:
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create_user(
            email=email, username=username, password=password
        )
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return HttpResponse("Error")
    else:
        return render(request, "frugal/register.html")


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


# saves linked products under a unique favorite id
@login_required(redirect_field_name="")
def favorite_view(request):
    if request.POST:
        favorite = save_to_favorite_and_products(request)
        return HttpResponseRedirect(reverse("details", args=(favorite.pk,)))


# displays all logged in user's favorites
@login_required(redirect_field_name="")
def favorites_view(request):
    is_ajax_request = request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
    if is_ajax_request:
        search_param = request.POST.get("search_param")
        filtered_favorites = Favorite.objects.filter(
            name__icontains=search_param, user_id=request.user.id
        )

        html = render_to_string(
            template_name="frugal/favorites-results.html",
            context={"user_favorites": filtered_favorites},
        )

        data_dict = {"html_from_view": html}
        
        return JsonResponse(data=data_dict)
    else:
        user_favorites = Favorite.objects.filter(user_id=request.user.id)
        context = {"user_favorites": user_favorites}

        return render(request, "frugal/favorites.html", context)


# displays all details for given favorite id
@login_required(redirect_field_name="")
def favorite_details(request, favorite_id):
    if request.POST:
        user_favorite = Favorite.objects.get(pk=favorite_id)
        user_favorited_products = Product.objects.filter(favorite_id=favorite_id)
        update_product_prices(user_favorite, user_favorited_products)

        updated_user_favorite = Favorite.objects.get(pk=favorite_id)
        updated_user_favorited_products = Product.objects.filter(
            favorite_id=favorite_id
        )
        context = {
            "user_favorite": updated_user_favorite,
            "user_favorited_products": updated_user_favorited_products,
        }

        return HttpResponseRedirect(reverse("details", args=(favorite_id,)))

    else:
        user_favorite = Favorite.objects.get(pk=favorite_id)
        user_favorited_products = Product.objects.filter(favorite_id=favorite_id)
        context = {
            "user_favorite": user_favorite,
            "user_favorited_products": user_favorited_products,
        }

    return render(request, "frugal/details.html", context)


# checks if favorite was created by user before deleting
@login_required(redirect_field_name="")
def favorite_delete(request, favorite_id):
    is_ajax_request = request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
    if is_ajax_request:
        id = request.POST.get("favorite_id")
        favorite = Favorite.objects.get(pk=id, user_id=request.user.id)
        
        favorite.delete()

        search_param = request.POST.get("search_param")
        filtered_favorites = Favorite.objects.filter(name__icontains=search_param)

        html = render_to_string(
            template_name="frugal/favorites-results.html",
            context={"user_favorites": filtered_favorites},
        )

        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict)
    
@login_required(redirect_field_name="")
def recipes_view(request):
    return HttpResponse("Recipes")