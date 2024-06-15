from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, BillingForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Profile

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        #Get the order
        order = Order.objects.get(id=pk)
        #Get the order items
        items = OrderItem.objects.filter(order=pk)
        
        return render(request, "payment/orders.html", {"order":order, "items":items})

    else:
        messages.success(request, "Access Denied")
        return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        return render(request, "payment/not_shipped_dash.html", {"orders":orders})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        return render(request, "payment/shipped_dash.html", {"orders":orders})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')

def process_order(request):
    if request.POST:
        #Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        fee = 5
        end_total = totals + fee

        #Get billing info from the last page
        payment_form = BillingForm(request.POST or None)
        #Get shipping session data
        my_shipping = request.session.get('my_shipping')

        #Gather order info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        
        #Create shipping address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_postcode']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}"
        amount_paid = end_total

        #Create an order
        if request.user.is_authenticated:
            #If logged in
            user = request.user
            #Create order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            #Add order items
            #Get the order ID
            order_id = create_order.pk

            #Get product info
            for product in cart_products():
                #Get product ID
                product_id = product.id
                #Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                #Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        #Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()

            #Delete cart after order placed
            for key in list(request.session.keys()):
                if key == "session_key":
                    #Delete the key
                    del request.session[key]

            #Delete cart from database
            current_user = Profile.objects.filter(user__id=request.user.id)
            #Delete shopping cart data in database
            current_user.update(old_cart="")

            messages.success(request, "Order Placed! Kindly Prepare The Exact Amount For Payment Upon Delivery.")
            return redirect('home')

        else:
            #Not logged in
            #Create order
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            #Add order items
            #Get the order ID
            order_id = create_order.pk

            #Get product info
            for product in cart_products():
                #Get product ID
                product_id = product.id
                #Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                #Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        #Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()

            #Delete cart after order placed
            for key in list(request.session.keys()):
                if key == "session_key":
                    #Delete the key
                    del request.session[key]

            messages.success(request, "Order Placed! Kindly Prepare The Exact Amount For Payment Upon Delivery.")
            return redirect('home')

    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def billing_info(request):
    if request.POST:
        #Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        fee = 5
        end_total = totals + fee

        #Create a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        #Check to see if user is logged in
        if request.user.is_authenticated:
            #Get billing form
            billing_form = BillingForm()
            return render (request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form, "end_total":end_total })
        
        else:
            #Not logged in
            billing_form = BillingForm()
            return render (request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form, "end_total":end_total })
	
    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        #Checkout as logged in user
        #Shipping User
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
	    #Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render (request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    else:
        #Checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render (request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})


def payment_success(request):
    return render(request, "payment/payment_success.html", {})