from django.shortcuts import render

from django.http import HttpResponse

## home page
def home(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>Home page </h1>')

## register page
def register(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>register page </h1>')

## catalog page
def catalog(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>catalog page </h1>')

## listing page
def listing(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>listing page </h1>')

## cart page
def cart(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>cart page </h1>')

## checkout page
def checkout(request):
    ## return render(request, 'home.html')
    return HttpResponse('<h1>checkout page </h1>')