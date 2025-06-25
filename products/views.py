from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Category, ProductImage
from .forms import ProductForm, CategoryForm, ProductImageForm
from accounts.decorators import superadmin_required

# Public Views
def home(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')

    products = Product.objects.filter(is_active=True)
    if search_query:
        products = products.filter(product_name__icontains=search_query)
    if category_filter:
        products = products.filter(category_id=category_filter)

    categories = Category.objects.all()
    return render(request, 'products/home.html', {'products': products, 'categories': categories})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})


# Superadmin Views

@superadmin_required
def admin_product_list(request):
    products = Product.objects.all()
    return render(request, 'products/admin_product_list.html', {'products': products})


@superadmin_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('admin_product_list')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})


@superadmin_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('admin_product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form})


@superadmin_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('admin_product_list')


@superadmin_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('admin_product_list')
    else:
        form = CategoryForm()
    return render(request, 'products/add_category.html', {'form': form})



from PIL import Image
@superadmin_required
def upload_product_image(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            product_image = form.save(commit=False)
            product_image.product = product
            product_image.save()

            # Resize the image
            img_path = product_image.image.path
            img = Image.open(img_path)
            img = img.resize((500, 500))  # Resize to 500x500 pixels
            img.save(img_path)

            messages.success(request, 'Image uploaded and resized successfully.')
            return redirect('admin_product_list')
    else:
        form = ProductImageForm()

    return render(request, 'products/upload_product_image.html', {'form': form, 'product': product})