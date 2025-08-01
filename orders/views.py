from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CheckoutForm
from .models import Order, OrderItem
from carts.models import Cart, CartItem
from carts.views import _get_cart # Reuse cart retrieval logic
from django.db import transaction

def checkout(request):
    cart = _get_cart(request)
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty. Please add products before checking out.")
        return redirect('view_cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    if request.user.is_authenticated:
                        order.user = request.user
                    order.save()

                    for item in cart.items.all():
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            price=item.product.price, # Capture current price
                            quantity=item.quantity
                        )
                        # Optionally decrement product stock here
                        item.product.stock -= item.quantity
                        item.product.save()

                    cart.items.all().delete() # Clear the cart

                    messages.success(request, 'Your order has been placed successfully!')
                    return redirect('order_confirmation', order_id=order.id)
            except Exception as e:
                messages.error(request, f"There was an error processing your order: {e}")
                # Log the error for debugging
                print(f"Checkout error: {e}")
                return render(request, 'orders/checkout.html', {'form': form, 'cart_items': cart.items.all()})
    else:
        # Pre-fill form for logged-in users
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                # Add other user profile fields if available
            }
        form = CheckoutForm(initial=initial_data)

    cart_items = cart.items.all()
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'orders/checkout.html', {'form': form, 'cart_items': cart_items, 'total_price': total_price})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Ensure the user who placed the order (if logged in) or session matches (for guest)
    if request.user.is_authenticated and order.user != request.user:
        messages.error(request, "You are not authorized to view this order.")
        return redirect('home')
    # For guest users, you might want to store order ID in session for retrieval
    # or rely solely on direct link after checkout.
    
    order_items = order.items.all()
    return render(request, 'orders/order_confirmation.html', {'order': order, 'order_items': order_items})

def admin_order_list(request):
    # This view would typically be restricted to staff/admin users
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'orders/admin_order_list.html', {'orders': orders})