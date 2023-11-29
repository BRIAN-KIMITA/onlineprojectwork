from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import NewItemForm, EditItemForm, CheckoutForm

from .models import Category, Item, CartItem
from django.shortcuts import render


# @login_required
# def add_to_cart(request, pk):
#     item = get_object_or_404(Item, pk=pk)
#     name = item.name
#     price = item.price
#
#     # Check if the item is already in the cart
#     cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item, name=name, price=price)
#
#     if not created:
#         cart_item.name = name
#         cart_item.price = price
#         cart_item.quantity += 1
#         cart_item.save()
#
#     messages.success(request, f"{item.name} added to cart.")
#     return redirect('item:items')  # Update with your URL name for the item listing
#
#
# @login_required
# def view_cart(request):
#     cart_items = CartItem.objects.filter(user=request.user)
#     return render(request, 'item/cart.html', {'cart_items': cart_items})


# @login_required
# def remove_from_cart(request, pk):
#     cart_item = get_object_or_404(CartItem, pk=pk)
#     cart_item.delete()
#     messages.success(request, "Item removed from cart.")
#     return redirect('item:view_cart')


def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })


@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })


@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=pk)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })


@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)

    # Check if the item is already in the cart
    cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{item.name} added to cart.")
    return redirect('item:items')  # Update with your URL name for the item listing


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'item/cart.html', {'cart_items': cart_items})


@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('item:view_cart')


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items:
        # Handle the case where the cart is empty
        return redirect('item:view_cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Process the payment (for M-Pesa, you might send a payment request here)

            # Once payment is successful, mark items as sold and clear the cart
            for cart_item in cart_items:
                cart_item.item.is_sold = True
                cart_item.item.save()

            cart_items.delete()  # Clear the cart
            return render(request, 'item/checkout_success.html')
    else:
        form = CheckoutForm()

    return render(request, 'item/checkout.html', {'form': form, 'cart_items': cart_items})


def checkout_success(request):
    return render(request, 'item/checkout_success.html')


def checkout_cancel(request):
    return render(request, 'item/checkout_cancel.html')

# views.py
