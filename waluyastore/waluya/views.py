from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Fish, FishMedicine, AquariumStuff, FishFood, Wishlist, Product
from .forms import FishForm, FishMedicineForm, AquariumStuffForm, FishFoodForm, AdminLoginForm, UserSignupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from .forms import MessageForm
from .models import Message 
from django.contrib import messages as flash_messages 

# ==================== USER MANAGEMENT ====================

def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
    else:
        form = UserSignupForm()
    return render(request, 'sign_up.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                form.add_error('email', 'Email tidak ditemukan')
                return render(request, 'login.html', {'form': form})

            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('product_list')
                else:
                    return redirect('landing_page')
            else:
                form.add_error('password', 'Password salah')
    else:
        form = AdminLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('landing_page')

# ==================== LANDING PAGE ====================

def landing_page(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('product_list')
    return render(request, 'landing_page.html')

# ==================== WISHLIST ====================

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, f"{product.name} berhasil ditambahkan ke wishlist.")
    else:
        messages.warning(request, f"{product.name} sudah ada di wishlist.")
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    messages.info(request, f"{wishlist_item.product.name} dihapus dari wishlist.")
    wishlist_item.delete()
    return redirect('wishlist')


@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

# ==================== ADMIN CRUD (SUPERUSER ONLY) ====================

@login_required
def product_list(request):
    if not request.user.is_superuser:
        return redirect('user_product_list')
    
    category = request.GET.get('category', 'Fish')

    if category == 'Fish':
        products = Fish.objects.all()
    elif category == 'FishMedicine':
        products = FishMedicine.objects.all()
    elif category == 'AquariumStuff':
        products = AquariumStuff.objects.all()
    elif category == 'FishFood':
        products = FishFood.objects.all()
    else:
        products = Product.objects.none()

    return render(request, 'product_list_admin.html', {'products': products, 'category': category})

@login_required
def add_product(request):
    category = request.POST.get('category', 'Fish')

    form_classes = {
        'Fish': FishForm,
        'FishMedicine': FishMedicineForm,
        'AquariumStuff': AquariumStuffForm,
        'FishFood': FishFoodForm
    }
    form = form_classes.get(category, FishForm)(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        return redirect('product_list')

    return render(request, 'product_list_admin.html', {'form': form, 'category': category})

@login_required
def edit_product(request, product_id):
    category = request.GET.get('category', 'Fish')

    model_classes = {
        'Fish': Fish,
        'FishMedicine': FishMedicine,
        'AquariumStuff': AquariumStuff,
        'FishFood': FishFood
    }
    product = get_object_or_404(model_classes.get(category, Fish), id=product_id)
    form_classes = {
        'Fish': FishForm,
        'FishMedicine': FishMedicineForm,
        'AquariumStuff': AquariumStuffForm,
        'FishFood': FishFoodForm
    }
    form = form_classes.get(category, FishForm)(request.POST or None, request.FILES or None, instance=product)

    if form.is_valid():
        form.save()
        return redirect('product_list')

    return render(request, 'product_list_admin.html', {'form': form, 'category': category, 'product': product})

@login_required
def delete_product(request, product_id):
    category = request.GET.get('category', 'Fish')

    model_classes = {
        'Fish': Fish,
        'FishMedicine': FishMedicine,
        'AquariumStuff': AquariumStuff,
        'FishFood': FishFood
    }
    product = get_object_or_404(model_classes.get(category, Fish), id=product_id)
    messages.info(request, f"Produk {product.name} berhasil dihapus.")
    product.delete()
    return redirect('product_list')

# ==================== USER BROWSE PRODUCTS ====================
@login_required
def product_detail(request, product_id):
    for model_class, product_type in [
        (Fish, "Fish"),
        (FishMedicine, "FishMedicine"),
        (AquariumStuff, "AquariumStuff"),
        (FishFood, "FishFood")
    ]:
        try:
            product = model_class.objects.get(id=product_id)
            return render(request, 'product_detail.html', {
                'product': product,
                'product_type': product_type
            })
        except model_class.DoesNotExist:
            continue
    return HttpResponse("Product not found", status=404)


@login_required
def user_product_list(request):
    category = request.GET.get('category', 'Fish')
    search_query = request.GET.get('search', '')
    order_by = request.GET.get('order_by', '')
    filter_size = request.GET.get('size', '')
    filter_color = request.GET.get('color', '')
    filter_medicine_type = request.GET.get('medicine_type', '')
    filter_stuff_type = request.GET.get('stuff_type', '')
    filter_food_type = request.GET.get('food_type', '')

    if category == 'Fish':
        products = Fish.objects.all()
        if search_query:
            products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
        if filter_size:
            products = products.filter(size=filter_size)
        if filter_color:
            products = products.filter(color=filter_color)
    elif category == 'FishMedicine':
        products = FishMedicine.objects.all()
        if search_query:
            products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
        if filter_medicine_type:
            products = products.filter(medicine_type=filter_medicine_type)
    elif category == 'AquariumStuff':
        products = AquariumStuff.objects.all()
        if search_query:
            products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
        if filter_stuff_type:
            products = products.filter(stuff_type=filter_stuff_type)
    elif category == 'FishFood':
        products = FishFood.objects.all()
        if search_query:
            products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
        if filter_food_type:
            products = products.filter(food_type=filter_food_type)
    else:
        products = Product.objects.none()

    # 🔎 Search logic
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    # 🔃 Sorting logic
    if order_by == 'name_asc':
        products = products.order_by('name')
    elif order_by == 'name_desc':
        products = products.order_by('-name')
    elif order_by == 'price_asc':
        products = products.order_by('price')
    elif order_by == 'price_desc':
        products = products.order_by('-price')

    return render(request, 'user_product_list.html', {'products': products, 'category': category})

@login_required
def contact_admin(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.user = request.user
            msg.save()
            flash_messages.success(request, "Pesan berhasil dikirim ke admin!")
            return redirect('contact_admin')
    else:
        form = MessageForm(initial={'email': request.user.email})
    return render(request, 'contact_admin.html', {'form': form})



