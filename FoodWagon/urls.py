"""FoodWagon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from foodwagon_backend import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include

urlpatterns = [
    path('', views.index, name='index'),
    path('adminlogin/', views.adminlogin),
    path('catering/', views.catering),
    path('restaurent/', views.restaurent),
    path('venue/', views.venue),
    path('foodtruck/', views.foodtruck),
    path('chef/', views.chef),
    path('login/', views.loginPage, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name="logout"),
    path('admin/', admin.site.urls),
    path('venue/<int:id>', views.venuebyid),
    path('add_to_cart_venue/<int:id>', views.add_to_cart_venue),
    path('add_to_cart_truck/<int:id>', views.add_to_cart_truck),
    path('add_to_cart_chef/<int:id>', views.add_to_cart_chef),
    path('foodtruck/<int:id>', views.truckbyid),
    path('service/', views.service),
    path('catering/<int:id>', views.chefbyid),
    path('cart/', views.cart),
    path('reset-password/', PasswordResetView.as_view(
        template_name="FoodWagon/password-reset.html"), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='FoodWagon/password-reset-sent.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>[0-9A-Za-z]+)-<token>/',
         PasswordResetConfirmView.as_view(template_name='FoodWagon/password-reset-form.html'), name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='FoodWagon/password-reset-done.html'), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)