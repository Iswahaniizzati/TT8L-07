from django.shortcuts import render, redirect
from .models import Product, Categories, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms

def update_info(request):
    if request.user.is_authenticated:
        #Get Current User
        current_user = Profile.objects.get(user__id=request.user.id)
        #Get Current User's Shipping Info
        shipping_user = ShippingAddress.objects.get(id=request.user.id)
        
        #Get Original User Form
        form = UserInfoForm(request.POST or None, instance=current_user)
        #Get User's Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Info Has Been Updated!")
            return redirect('home')
        return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form})
    else:        
        messages.success(request, "You Must Be Logged In to Access That Page!")
        return redirect('home')



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

def register_user(request):
      form = SignUpForm()
      if request.method == "POST":
          form = SignUpForm(request.POST)
          if form.is_valid():
              form.save()
              username = form.cleaned_data['username']
              password = form.cleaned_data['password1']
              # log in user
              user = authenticate(username=username, password=password)
              login(request, user)
              messages.success(request, ("Username Created - Please Fill Out Your User Info Below..."))
              return redirect ('update_info')
          else: 
               messages.success(request, ("Whoops! There was a problem registering,please try again"))
               return redirect ('register')
      else:
            return render(request, 'register.html', {'form':form})