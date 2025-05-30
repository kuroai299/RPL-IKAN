from django.contrib import admin
from django.urls import path
from waluya import views  # pastikan ini mengarah ke folder yang benar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),  # URL default untuk Django Admin
    
    # User and Authentication
    path('', views.landing_page, name='landing_page'),  # Landing page untuk semua user
    path('login/', views.user_login, name='user_login'),  # Login untuk semua pengguna
    path('sign_up/', views.user_signup, name='sign_up'),  # Sign-up hanya untuk user biasa
    path('logout/', views.logout_view, name='logout'),  # Logout untuk semua user

    # Admin Dashboard (Custom Dashboard untuk Admin, jangan duplikasi dengan /admin/)
    path('custom-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Hanya untuk admin, URL custom
    # Hindari 'admin/' karena sudah dipakai oleh django admin
    path('custom-admin/add_product/', views.add_product, name='add_product'),
    path('custom-admin/edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('custom-admin/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),


    # Product Management (CRUD for Admin) - Operasi untuk admin
    #path('admin/add_product/', views.add_product, name='add_product'),
    #path('admin/edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    #path('admin/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),

    # Wishlist for users
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # New AJAX endpoints for wishlist
    path('check_wishlist/<int:product_id>/', views.check_wishlist, name='check_wishlist'),

    # Product Detail for Users
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Product Categories for Users
    path('ikan/', views.user_product_list_ikan, name='user_product_list_ikan'),  # Kategori Ikan
    path('obat_ikan/', views.user_product_list_obat_ikan, name='user_product_list_obat_ikan'),  # Kategori Obat Ikan
    path('barang_akuarium/', views.user_product_list_barang_akuarium, name='user_product_list_barang_akuarium'),  # Kategori Barang Akuarium
    path('makanan_ikan/', views.user_product_list_makanan_ikan, name='user_product_list_makanan_ikan'),  # Kategori Makanan Ikan

    
    path('api/product/<int:product_id>/', views.product_detail_api, name='product_detail_api'),


    # Contact admin (for sending messages to admin)
    path('contact_admin/', views.contact_admin, name='contact_admin'),
    path('admin_message/', views.admin_message, name='admin_message'),
    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)