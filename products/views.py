from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Category, ProductImage
from .forms import ProductForm, CategoryForm, ProductImageForm
from accounts.decorators import superadmin_required
import os
from PIL import Image

# --- Public Views ---

def user_home(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')

    products = Product.objects.filter(is_active=True)
    if search_query:
        products = products.filter(product_name__icontains=search_query)
    if category_filter:
        products = products.filter(category_id=category_filter)

    categories = Category.objects.all()
    return render(request, 'products/user_home.html', {'products': products, 'categories': categories})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})


# --- Superadmin Views ---

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
    return render(request, 'products/admin_add_product.html', {'form': form})


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
    return render(request, 'products/admin_edit_product.html', {
        'form': form,
        'product': product
    })

@superadmin_required
def delete_product_image(request, image_id):
    image = get_object_or_404(ProductImage, id=image_id)
    product_id = image.product.id

    if image.image and os.path.isfile(image.image.path):
        os.remove(image.image.path)

    image.delete()
    messages.success(request, "Image deleted successfully.")
    return redirect('edit_product', product_id=product_id)

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
            img = img.resize((500, 500))
            img.save(img_path)

            messages.success(request, 'Image uploaded and resized successfully.')
            return redirect('admin_product_list')
    else:
        form = ProductImageForm()

    return render(request, 'products/admin_upload_product_image.html', {
        'form': form,
        'product': product
    })

@superadmin_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('admin_product_list')


@superadmin_required
@superadmin_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('add_category')
    else:
        form = CategoryForm()

    # ✅ Always fetch categories
    categories = Category.objects.all()
    return render(request, 'products/admin_add_category.html', {
        'form': form,
        'categories': categories
    })


@superadmin_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, "Category deleted successfully.")
    return redirect('add_category')

@superadmin_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('add_category')
    else:
        form = CategoryForm(instance=category)

    categories = Category.objects.all()
    return render(request, 'products/admin_add_category.html', {
        'form': form,
        'categories': categories
    })