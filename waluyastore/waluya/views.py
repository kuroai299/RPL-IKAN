from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Fish, FishMedicine, AquariumStuff, FishFood, Wishlist, Product
from .forms import FishForm, FishMedicineForm, AquariumStuffForm, FishFoodForm, AdminLoginForm, UserSignupForm, MessageForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET

# ==================== USER MANAGEMENT ====================

def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Simpan user baru
            login(request, user)  # Login otomatis setelah registrasi
            return redirect('landing_page')  # Arahkan ke halaman landing setelah sukses signup
    else:
        form = UserSignupForm()  # Jika GET, tampilkan form kosong
    
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
                    return redirect('admin_dashboard')
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
            return redirect('admin_dashboard')
    return render(request, 'landing_page.html')

# ==================== WISHLIST ====================

@login_required
def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    Wishlist.objects.create(user=request.user, product=product)
    return redirect('wishlist')

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def remove_from_wishlist(request, wishlist_id):
    try:
        wishlist_item = Wishlist.objects.get(id=wishlist_id, user=request.user)
        wishlist_item.delete()
        messages.success(request, "Produk berhasil dihapus dari wishlist.")
    except Wishlist.DoesNotExist:
        messages.error(request, "Produk tidak ditemukan di wishlist.")
    
    return redirect('wishlist')

# ==================== ADMIN DASHBOARD ====================

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('landing_page')

    category = request.GET.get('category', 'Fish')
    format_type = request.GET.get('format', 'html')
    search_query = request.GET.get('search', '')

    model_classes = {
        'Fish': Fish,
        'FishMedicine': FishMedicine,
        'AquariumStuff': AquariumStuff,
        'FishFood': FishFood,
    }

    products = model_classes.get(category, Fish).objects.all()
    
    # Apply search filter if provided
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Return JSON if requested
    if format_type == 'json':
        products_data = []
        for product in products:
            product_data = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': str(product.price),
                'stock': product.stock,
                'image': product.image.url if product.image else '/static/images/no-image.png',
                'category': category,
            }
            
            # Add category-specific fields
            if category == 'Fish':
                product_data['size'] = product.size
                product_data['color'] = product.color
            elif category == 'FishMedicine':
                product_data['medicine_type'] = product.medicine_type
            elif category == 'AquariumStuff':
                product_data['stuff_type'] = product.stuff_type
            elif category == 'FishFood':
                product_data['food_type'] = product.food_type
                
            products_data.append(product_data)
            
        return JsonResponse({'products': products_data})

    # Return HTML for normal requests
    models_info = [
        {'name': 'Fish', 'add_url': f'/add_product/?category=Fish', 'change_url': f'/custom-admin/dashboard/?category=Fish'},
        {'name': 'Fish Medicine', 'add_url': f'/add_product/?category=FishMedicine', 'change_url': f'/custom-admin/dashboard/?category=FishMedicine'},
        {'name': 'Aquarium Stuff', 'add_url': f'/add_product/?category=AquariumStuff', 'change_url': f'/custom-admin/dashboard/?category=AquariumStuff'},
        {'name': 'Fish Food', 'add_url': f'/add_product/?category=FishFood', 'change_url': f'/custom-admin/dashboard/?category=FishFood'},
        {'name': 'Message', 'add_url': '#', 'change_url': '/admin/waluya/message/'},
    ]

    return render(request, 'admin_dashboard.html', {
        'models_info': models_info,
        'products': products,
        'category': category,
    })

@login_required
def add_product(request):
    if not request.user.is_superuser:
        return redirect('landing_page')
    
    if request.method == 'POST':
        category = request.POST.get('category', 'Fish')
        
        # Debug output
        print("Form data received:")
        for key, value in request.POST.items():
            print(f"{key}: {value}")
        
        if request.FILES:
            print("Files received:")
            for key, value in request.FILES.items():
                print(f"{key}: {value.name} ({value.size} bytes)")
        
        form_classes = {
            'Fish': FishForm,
            'FishMedicine': FishMedicineForm,
            'AquariumStuff': AquariumStuffForm,
            'FishFood': FishFoodForm
        }
        
        form_class = form_classes.get(category, FishForm)
        form = form_class(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                product = form.save()
                
                # Return JSON response if requested
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True, 
                        'product_id': product.id,
                        'message': 'Product added successfully'
                    })
                
                messages.success(request, f"Produk {product.name} berhasil ditambahkan.")
                return redirect('admin_dashboard')
            except Exception as e:
                print(f"Error saving product: {str(e)}")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False, 
                        'error': f'Error saving product: {str(e)}'
                    }, status=500)
        else:
            print("Form validation errors:")
            for field, errors in form.errors.items():
                print(f"{field}: {errors}")
            
            # Return form errors as JSON if requested
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False, 
                    'error': 'Form validation failed',
                    'errors': {field: str(errors[0]) for field, errors in form.errors.items()}
                }, status=400)
    
    # For GET requests
    # ...rest of your code
    
@login_required
def edit_product(request, product_id):
    if not request.user.is_superuser:
        return redirect('landing_page')
    
    category = request.GET.get('category', 'Fish')
    
    model_classes = {
        'Fish': Fish,
        'FishMedicine': FishMedicine,
        'AquariumStuff': AquariumStuff,
        'FishFood': FishFood
    }
    
    try:
        product = get_object_or_404(model_classes.get(category, Fish), id=product_id)
    except:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)
        return redirect('admin_dashboard')
    
    form_classes = {
        'Fish': FishForm,
        'FishMedicine': FishMedicineForm,
        'AquariumStuff': AquariumStuffForm,
        'FishFood': FishFoodForm
    }
    
    if request.method == 'POST':
        form = form_classes.get(category, FishForm)(
            request.POST, request.FILES, instance=product
        )
        
        if form.is_valid():
            product = form.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'product_id': product.id,
                    'message': 'Product updated successfully'
                })
            
            messages.success(request, f"Produk {product.name} berhasil diperbarui.")
            return redirect('admin_dashboard')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False, 
                    'error': 'Form validation failed',
                    'errors': {field: errors[0] for field, errors in form.errors.items()}
                }, status=400)
    
    # If GET request or non-AJAX response
    form = form_classes.get(category, FishForm)(instance=product)
    
    # If AJAX request, return product data as JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),
            'stock': product.stock,
            'image': product.image.url if product.image else None,
            'category': category,
        }
        
        # Add category-specific fields
        if category == 'Fish':
            product_data['size'] = product.size
            product_data['color'] = product.color
        elif category == 'FishMedicine':
            product_data['medicine_type'] = product.medicine_type
        elif category == 'AquariumStuff':
            product_data['stuff_type'] = product.stuff_type
        elif category == 'FishFood':
            product_data['food_type'] = product.food_type
            
        return JsonResponse({'success': True, 'product': product_data})
    
    return render(request, 'admin_dashboard.html', {
        'form': form, 
        'category': category, 
        'product': product
    })

@login_required
def delete_product(request, product_id):
    if not request.user.is_superuser:
        return redirect('landing_page')
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    category = request.GET.get('category', 'Fish')
    
    model_classes = {
        'Fish': Fish,
        'FishMedicine': FishMedicine,
        'AquariumStuff': AquariumStuff,
        'FishFood': FishFood
    }
    
    try:
        product = get_object_or_404(model_classes.get(category, Fish), id=product_id)
        product_name = product.name
        product.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True, 
                'message': f'Product {product_name} deleted successfully'
            })
        
        messages.success(request, f"Produk {product_name} berhasil dihapus.")
        return redirect('admin_dashboard')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False, 
                'error': str(e)
            }, status=500)
        
        messages.error(request, f"Gagal menghapus produk: {str(e)}")
        return redirect('admin_dashboard')

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

# ==================== CONTACT ADMIN ====================

@login_required
def contact_admin(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.user = request.user
            msg.save()
            messages.success(request, "Pesan berhasil dikirim ke admin!")
            return redirect('contact_admin')
    else:
        form = MessageForm(initial={'email': request.user.email})
    return render(request, 'contact_admin.html', {'form': form})

# ==================== USER PRODUCT LISTS ====================

def user_product_list_ikan(request):
    search_query = request.GET.get('search', '')
    order_by = request.GET.get('order_by', '')
    filter_size = request.GET.get('size', '')
    filter_color = request.GET.get('color', '')

    products = Fish.objects.all()
    if search_query:
        products = products.filter(name__icontains=search_query)
    if filter_size:
        products = products.filter(size=filter_size)
    if filter_color:
        products = products.filter(color=filter_color)

    # Sorting logic
    if order_by == 'name_asc':
        products = products.order_by('name')
    elif order_by == 'name_desc':
        products = products.order_by('-name')
    elif order_by == 'price_asc':
        products = products.order_by('price')
    elif order_by == 'price_desc':
        products = products.order_by('-price')

    return render(request, 'user_product_list_ikan.html', {'products': products})

def user_product_list_obat_ikan(request):
    search_query = request.GET.get('search', '')
    order_by = request.GET.get('order_by', '')
    filter_medicine_type = request.GET.get('medicine_type', '')

    products = FishMedicine.objects.all()
    if search_query:
        products = products.filter(name__icontains=search_query)
    if filter_medicine_type:
        products = products.filter(medicine_type=filter_medicine_type)

    # Sorting logic
    if order_by == 'name_asc':
        products = products.order_by('name')
    elif order_by == 'name_desc':
        products = products.order_by('-name')
    elif order_by == 'price_asc':
        products = products.order_by('price')
    elif order_by == 'price_desc':
        products = products.order_by('-price')

    return render(request, 'user_product_list_obat_ikan.html', {'products': products})

def user_product_list_barang_akuarium(request):
    search_query = request.GET.get('search', '')
    order_by = request.GET.get('order_by', '')
    filter_stuff_type = request.GET.get('stuff_type', '')

    products = AquariumStuff.objects.all()  # Ambil semua produk dari kategori AquariumStuff
    if search_query:
        products = products.filter(name__icontains=search_query)  # Filter berdasarkan nama produk
    if filter_stuff_type:
        products = products.filter(stuff_type=filter_stuff_type)  # Filter berdasarkan jenis stuff

    # Sorting logic
    if order_by == 'name_asc':
        products = products.order_by('name')
    elif order_by == 'name_desc':
        products = products.order_by('-name')
    elif order_by == 'price_asc':
        products = products.order_by('price')
    elif order_by == 'price_desc':
        products = products.order_by('-price')

    return render(request, 'user_product_list_barang_akuarium.html', {'products': products})

def user_product_list_makanan_ikan(request):
    search_query = request.GET.get('search', '')
    order_by = request.GET.get('order_by', '')
    filter_food_type = request.GET.get('food_type', '')

    products = FishFood.objects.all()  # Ambil semua produk Makanan Ikan
    if search_query:
        products = products.filter(name__icontains=search_query)  # Filter berdasarkan nama produk
    if filter_food_type:
        products = products.filter(food_type=filter_food_type)  # Filter berdasarkan jenis makanan ikan

    # Sorting logic
    if order_by == 'name_asc':
        products = products.order_by('name')
    elif order_by == 'name_desc':
        products = products.order_by('-name')
    elif order_by == 'price_asc':
        products = products.order_by('price')
    elif order_by == 'price_desc':
        products = products.order_by('-price')

    return render(request, 'user_product_list_makanan_ikan.html', {'products': products})

@login_required
@require_GET
def product_detail_api(request, product_id):
    # Coba ambil produk dari semua kategori (modifikasi sesuai kebutuhan)
    for model_class in [Fish, FishMedicine, AquariumStuff, FishFood]:
        try:
            product = model_class.objects.get(id=product_id)
            data = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': str(product.price),
                'category': model_class.__name__,
                'image_url': product.image.url if product.image else '',
                # Tambah field lain sesuai kebutuhan
            }
            return JsonResponse(data)
        except model_class.DoesNotExist:
            continue
    return JsonResponse({'error': 'Product not found'}, status=404)