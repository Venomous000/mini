from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from accounts.decorators import superadmin_required
from accounts.models import Address
from products.models import Product

# User Views
@login_required
def place_order(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not CartItem.objects.filter(cart=cart).exists():
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    # Create Order
    order = Order.objects.create(user=request.user, total_amount=cart.total_price)

    # Move CartItems to OrderItems
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            unit_price=item.unit_price
        )
        item.delete()

    cart.total_price = 0.00
    cart.save()

    messages.success(request, "Order placed successfully!")
    return redirect('order_history')


@login_required
def place_buy_now_order(request):
    product_id = request.session.get('buy_now_product_id')
    if not product_id:
        messages.error(request, "No product selected for Buy Now.")
        return redirect('product_list')

    product = get_object_or_404(Product, id=product_id)

    if product.stock_quantity < 1:
        messages.error(request, "Product is out of stock.")
        return redirect('product_list')

    total_amount = product.price_per_piece

    # Create Order
    order = Order.objects.create(user=request.user, total_amount=total_amount)

    # Create OrderItem
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1,
        unit_price=product.price_per_piece
    )

    messages.success(request, "Order placed successfully with Buy Now!")
    del request.session['buy_now_product_id']
    return redirect('order_history')


@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order deleted successfully.')
        return redirect('order_history')

    return render(request, 'orders/confirm_delete_order.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'orders/order_history.html', {'orders': orders})



# Admin Views
@superadmin_required
def admin_order_list(request):
    query = request.GET.get('q')  # User Email
    city = request.GET.get('city')
    province = request.GET.get('province')
    country = request.GET.get('country')
    zip_code = request.GET.get('zip_code')

    orders = Order.objects.all().order_by('-order_date')

    if query:
        orders = orders.filter(user__email__icontains=query)

    if city or province or country or zip_code:
        orders = orders.filter(
            user__addresses__city__icontains=city if city else '',
            user__addresses__province__icontains=province if province else '',
            user__addresses__country__icontains=country if country else '',
            user__addresses__zip_code__icontains=zip_code if zip_code else '',
        ).distinct()

    return render(request, 'orders/admin_order_list.html', {
        'orders': orders,
        'query': query,
        'city': city,
        'province': province,
        'country': country,
        'zip_code': zip_code,
    })

@superadmin_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'orders/admin_order_detail.html', {'order': order, 'order_items': order_items})

@login_required
def buy_now(request, product_id):
    request.session['buy_now_product_id'] = product_id
    return redirect('checkout_buy_now')


@login_required
def checkout_buy_now(request):
    product_id = request.session.get('buy_now_product_id')
    if not product_id:
        messages.error(request, "No product selected for Buy Now.")
        return redirect('product_list')

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        return redirect('place_buy_now_order')

    return render(request, 'orders/checkout_buy_now.html', {'product': product})


@login_required
def place_buy_now_order(request):
    product_id = request.session.get('buy_now_product_id')
    if not product_id:
        messages.error(request, "No product selected for Buy Now.")
        return redirect('product_list')

    product = get_object_or_404(Product, id=product_id)

    if product.stock_quantity < 1:
        messages.error(request, "Product is out of stock.")
        return redirect('product_list')

    total_amount = product.price_per_piece

    # Create Order
    order = Order.objects.create(user=request.user, total_amount=total_amount)

    # Create OrderItem
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1,
        unit_price=product.price_per_piece
    )

    messages.success(request, "Order placed successfully with Buy Now!")
    del request.session['buy_now_product_id']
    return redirect('order_history')


@login_required
def cart_checkout(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not CartItem.objects.filter(cart=cart).exists():
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    cart_items = CartItem.objects.filter(cart=cart)

    if request.method == 'POST':
        return redirect('place_cart_order')

    return render(request, 'orders/cart_checkout.html', {'cart_items': cart_items, 'total_price': cart.total_price})



@login_required
def place_cart_order(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not CartItem.objects.filter(cart=cart).exists():
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    # Create Order
    order = Order.objects.create(user=request.user, total_amount=cart.total_price)

    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            unit_price=item.unit_price
        )
        item.delete()

    cart.total_price = 0.00
    cart.save()

    messages.success(request, "Order placed successfully!")
    return redirect('order_history')
