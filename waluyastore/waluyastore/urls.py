"""waluyastore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from waluya import views  # pastikan ini mengarah ke folder yang benar
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing_page'),  # Landing page untuk semua user
    path('login/', views.user_login, name='user_login'),  # Login untuk semua pengguna
    path('sign_up/', views.user_signup, name='user_signup'),  # Sign-up hanya untuk user biasa
    path('admin/product_list/', views.product_list, name='product_list'),  # Hanya untuk admin
    path('logout/', views.logout_view, name='logout'),  # Logout untuk semua user
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('user/product_list/', views.user_product_list, name='user_product_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

