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
    product = get_object_or_404(Product, id=product_id)

    if product.stock_quantity < 1:
        messages.error(request, "This product is currently out of stock.")
        return redirect('home')  # ✅ FIXED here

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={
            'unit_price': product.price_per_piece,
            'quantity': 1
        }
    )

    if not created:
        if cart_item.quantity < product.stock_quantity:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, "Product quantity updated in cart.")
        else:
            messages.warning(request, "You’ve already added the maximum quantity available in stock.")
    else:
        messages.success(request, "Product added to cart.")

    next_url = request.GET.get('next', '/products/')
    return redirect(next_url)


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

    if request.method == 'POST':
        cart_item.delete()
        messages.success(request, "Item removed from cart.")

        # Optional: Auto-delete empty cart
        cart = Cart.objects.get(user=request.user)
        if not CartItem.objects.filter(cart=cart).exists():
            cart.delete()

    return redirect('view_cart')


@login_required
def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity'))
        except (ValueError, TypeError):
            messages.error(request, "Invalid quantity.")
            return redirect('view_cart')

        if quantity < 1:
            cart_item.delete()
            messages.success(request, "Item removed from cart.")

            # Delete empty cart if no items left
            cart = Cart.objects.get(user=request.user)
            if not CartItem.objects.filter(cart=cart).exists():
                cart.delete()
            return redirect('view_cart')

        if quantity > cart_item.product.stock_quantity:
            messages.error(request, f"Only {cart_item.product.stock_quantity} items are in stock.")
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated successfully.")

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
