from django.shortcuts import render, redirect
from .models import Product, Categories
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages






def category(request,foo):
    #Replace hyphens with spaces
    foo = foo.replace('-',' ')
    #Grab the category from the url
    try:
        #Look up the category
        category = Categories.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
     messages.success(request,("Sorry, that category doesn't exist"))
     return redirect('home')

def product(request,pk):
     product = Product.objects.get(id=pk)
     return render(request, 'product.html', {'product': product})



def update_user(request):
    return render(request, 'update_user.html', {})

def home(request):
    products = Product.objects.all()
    categories = Categories.objects.all()
    return render(request, 'home.html', {'products': products, 'categories': categories})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("You have been logged in"))
            return redirect('home')
        else :
         messages.error(request,("There was an error, please try again"))
         return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out.Thanks for your visit!"))
    return redirect('home')