from django.contrib import admin
from django.urls import path, include
from waluya import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    # Password Reset URLs - Gunakan custom views Anda
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),name="password_reset"),
    path('password_reset/done/',auth_views.PasswordResetView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetView.as_view(template_name='complete.html'), name='password_reset_complete'),

    # Admin URLs
    path('admin/', admin.site.urls),
    
    # User and Authentication
    path('', views.landing_page, name='landing_page'),
    path('login/', views.user_login, name='user_login'),
    path('sign_up/', views.user_signup, name='sign_up'),
    path('logout/', views.logout_view, name='logout'),

    # Admin Dashboard
    path('custom-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('custom-admin/add_product/', views.add_product, name='add_product'),
    path('custom-admin/edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('custom-admin/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),

    # Wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('check_wishlist/<int:product_id>/', views.check_wishlist, name='check_wishlist'),

    # Products
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('ikan/', views.user_product_list_ikan, name='user_product_list_ikan'),
    path('obat_ikan/', views.user_product_list_obat_ikan, name='user_product_list_obat_ikan'),
    path('barang_akuarium/', views.user_product_list_barang_akuarium, name='user_product_list_barang_akuarium'),
    path('makanan_ikan/', views.user_product_list_makanan_ikan, name='user_product_list_makanan_ikan'),
    path('api/product/<int:product_id>/', views.product_detail_api, name='product_detail_api'),

    # Contact
    path('contact_admin/', views.contact_admin, name='contact_admin'),
    path('admin_message/', views.admin_message, name='admin_message'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)