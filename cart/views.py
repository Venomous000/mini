from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    for item in cart_items:
        item.total_price = item.unit_price * item.quantity 

    total_price = sum(item.total_price for item in cart_items)
    cart.total_price = total_price
    cart.save()

    return render(request, 'cart/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        if cart_item.quantity + 1 > product.stock_quantity:
            messages.error(request, f"Only {product.stock_quantity} items in stock.")
            return redirect('product_detail', product_id=product.id)
        cart_item.quantity += 1
    else:
        cart_item.unit_price = product.price_per_piece
        if 1 > product.stock_quantity:
            messages.error(request, f"Only {product.stock_quantity} items in stock.")
            return redirect('product_detail', product_id=product.id)

    cart_item.save()
    messages.success(request, f"{product.product_name} added to cart.")
    return redirect('view_cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    cart = Cart.objects.get(user=request.user)
    if not CartItem.objects.filter(cart=cart).exists():
        cart.delete()
        messages.success(request, "Item removed from cart.")
    return redirect('view_cart')


@login_required
def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if quantity > 0:
            # Add this stock check
            if quantity > cart_item.product.stock_quantity:
                messages.error(request, f"Only {cart_item.product.stock_quantity} items in stock.")
                return redirect('view_cart')

            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated successfully.")
        else:
            cart_item.delete()
            messages.success(request, "Item removed from cart.")

            # Optional: Auto-delete empty cart
            cart = Cart.objects.get(user=request.user)
            if not CartItem.objects.filter(cart=cart).exists():
                cart.delete()

    return redirect('view_cart')


@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)

    if product.stock_quantity < 1:
        messages.error(request, "Product is out of stock.")
        return redirect('product_detail', product_id=product.id)

    # Create a temporary cart or directly pass product to order
    request.session['buy_now_product_id'] = product.id
    return redirect('place_buy_now_order')
