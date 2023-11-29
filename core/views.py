from django.contrib.auth import logout
from django.shortcuts import render, redirect

from item.models import Category, Item

from .forms import SignupForm


def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })


def contact(request):
    return render(request, 'core/contact.html')


def about(request):
    return render(request, 'core/about.html')


def privacy(request):
    return render(request, 'core/privacy.html')


def terms(request):
    return render(request, 'core/terms.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })


def logout_view(request):
    # Log the user out
    logout(request)

    return redirect('/login')



def checkout_success(request):
    return render(request, 'checkout_success.html')


def checkout_cancel(request):
    return render(request, 'checkout_cancel.html')

# Other views...
