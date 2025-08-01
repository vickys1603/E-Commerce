from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from items.models import Product
from .models import Cart, CartItem
from django.db import transaction

def _get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        cart = _get_cart(request)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        # For AJAX requests, return JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Product added to cart!', 'cart_item_count': cart.items.count()})

        return redirect('view_cart')
    return redirect('home') # Or an error page

def view_cart(request):
    cart = _get_cart(request)
    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'carts/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

def update_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action') # 'increase', 'decrease', 'remove'

        cart_item = get_object_or_404(CartItem, id=item_id)
        
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
            else:
                cart_item.save()
        elif action == 'remove':
            cart_item.delete()
        
        # For AJAX requests, return JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            cart = _get_cart(request)
            cart_items_data = [{'id': item.id, 'product_name': item.product.name, 'quantity': item.quantity, 'price': str(item.product.price), 'total_price': str(item.get_total_price())} for item in cart.items.all()]
            total_price = sum(item.get_total_price() for item in cart.items.all())
            return JsonResponse({'message': 'Cart updated successfully!', 'cart_items': cart_items_data, 'total_price': str(total_price)})
            
        return redirect('view_cart')
    return redirect('view_cart')