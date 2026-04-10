from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
        return redirect('shop-home')
    else:
        form = UserCreationForm()


    return render(request, 'shop/register.html', {'form': form})

def login_view(request):
    next_url = request.GET.get('next', 'shop-home')  # Default to home if no next parameter
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('shop-home')
    else:
        form = AuthenticationForm()

    return render(request, 'shop/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('shop-home')