"""
URL configuration for frugalsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include
=======
from django.urls import include, path
>>>>>>> 9fd34bf (deleted apps and created all views in single app)

urlpatterns = [
    path("", include("frugal.urls")),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")), 
]
