from django.contrib import admin
from django.urls import path
from waluya import views  # pastikan ini mengarah ke folder yang benar
from django.conf import settings
from django.conf.urls.static import static

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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

