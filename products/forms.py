from django import forms
from .models import Product, Category, ProductImage

# Product Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'stock_quantity', 'price_per_piece', 'product_description', 'is_active']

# Category Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']

# Product Image Form
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
