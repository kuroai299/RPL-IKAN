from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Fish, FishMedicine, AquariumStuff, FishFood, Wishlist, Product
from .forms import FishForm, FishMedicineForm, AquariumStuffForm, FishFoodForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import AdminLoginForm, UserSignupForm  # Form untuk login admin dan sign-up user umum
from django.contrib.auth.models import User

@login_required
def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    Wishlist.objects.create(user=request.user, product=product)
    return redirect('wishlist')  # Redirect ke halaman wishlist setelah menambahkan produk

# View untuk melihat wishlist pengguna
@login_required
def wishlist(request):
    # Ambil semua produk di wishlist pengguna yang sedang login
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


# View untuk login
def user_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Cari pengguna berdasarkan email
            try:
                user = User.objects.get(email=email)  # Ambil pengguna berdasarkan email
            except User.DoesNotExist:
                form.add_error('email', 'Email tidak ditemukan')
                return render(request, 'login.html', {'form': form})

            # Autentikasi pengguna berdasarkan email dan password
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)  # Login pengguna

                # Cek apakah pengguna adalah superuser
                if user.is_superuser:
                    # Redirect ke halaman produk list admin jika superuser
                    return redirect('product_list')  # Langsung ke halaman admin
                else:
                    # Redirect ke halaman produk list user jika bukan superuser
                    return redirect('user_product_list')  # Redirect ke halaman produk untuk user
            else:
                form.add_error('password', 'Password salah')
                return render(request, 'login.html', {'form': form})

    else:
        form = AdminLoginForm()  # Form kosong untuk GET request

    return render(request, 'login.html', {'form': form})


# View untuk sign-up user biasa

def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()  # Menyimpan data pengguna ke database
            return redirect('user_login')  # Redirect ke login setelah sign-up
    else:
        form = UserSignupForm()

    return render(request, 'sign_up.html', {'form': form})

# View untuk logout
def logout_view(request):
    logout(request)
    return redirect('landing_page')

# View untuk landing page
def landing_page(request):
    return render(request, 'landing_page.html')

# Pastikan hanya admin yang bisa mengakses halaman produk
@login_required
@login_required
def product_list(request):
    if not request.user.is_superuser:
        return redirect('user_product_list')  # Redirect ke halaman produk untuk user jika bukan superuser
    
    category = request.GET.get('category', 'Fish')  # Default category is 'Fish'

    if category == 'Fish':
        products = Fish.objects.all()
    elif category == 'FishMedicine':
        products = FishMedicine.objects.all()
    elif category == 'AquariumStuff':
        products = AquariumStuff.objects.all()
    elif category == 'FishFood':
        products = FishFood.objects.all()

    return render(request, 'product_list_admin.html', {'products': products, 'category': category})


# View untuk menambah produk baru
def add_product(request):
    category = request.POST.get('category', 'Fish')
    
    if category == 'Fish':
        form = FishForm(request.POST, request.FILES)
    elif category == 'FishMedicine':
        form = FishMedicineForm(request.POST, request.FILES)
    elif category == 'AquariumStuff':
        form = AquariumStuffForm(request.POST, request.FILES)
    elif category == 'FishFood':
        form = FishFoodForm(request.POST, request.FILES)
    else:
        form = FishForm(request.POST, request.FILES)
    
    if form.is_valid():
        form.save()
        return redirect('product_list')  # Redirect to the product list page after saving the product
    
    return render(request, 'product_list.html', {'form': form, 'category': category})

# View untuk mengedit produk
def edit_product(request, product_id):
    category = request.GET.get('category', 'Fish')
    product = get_object_or_404(Fish, id=product_id) if category == 'Fish' else (
        get_object_or_404(FishMedicine, id=product_id) if category == 'FishMedicine' else (
        get_object_or_404(AquariumStuff, id=product_id) if category == 'AquariumStuff' else (
        get_object_or_404(FishFood, id=product_id))))
    
    if category == 'Fish':
        form = FishForm(request.POST or None, request.FILES or None, instance=product)
    elif category == 'FishMedicine':
        form = FishMedicineForm(request.POST or None, request.FILES or None, instance=product)
    elif category == 'AquariumStuff':
        form = AquariumStuffForm(request.POST or None, request.FILES or None, instance=product)
    elif category == 'FishFood':
        form = FishFoodForm(request.POST or None, request.FILES or None, instance=product)
    
    if form.is_valid():
        form.save()
        return redirect('product_list')  # Redirect to the product list page after saving the updated product

    return render(request, 'product_list.html', {'form': form, 'category': category, 'product': product})

# View untuk menghapus produk
def delete_product(request, product_id):
    category = request.GET.get('category', 'Fish')
    product = get_object_or_404(Fish, id=product_id) if category == 'Fish' else (
        get_object_or_404(FishMedicine, id=product_id) if category == 'FishMedicine' else (
        get_object_or_404(AquariumStuff, id=product_id) if category == 'AquariumStuff' else (
        get_object_or_404(FishFood, id=product_id))))
    
    product.delete()  # Delete the product from the database
    return redirect('product_list')  # Redirect to the product list page after deletion

def user_product_list(request):
    category = request.GET.get('category', 'Fish')  # Default category is 'Fish'

    if category == 'Fish':
        products = Fish.objects.all()
    elif category == 'FishMedicine':
        products = FishMedicine.objects.all()
    elif category == 'AquariumStuff':
        products = AquariumStuff.objects.all()
    elif category == 'FishFood':
        products = FishFood.objects.all()

    return render(request, 'user_product_list.html', {'products': products, 'category': category})
