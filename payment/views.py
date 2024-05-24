from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the order
        order = Order.objects.get(id=pk)
        # Get the order items
        items = OrderItem.objects.filter(order=pk)
        return render(request, 'payment/orders.html',{"order":order,"items":items})
    else:
        messages.success(request, "Order Denied")
        return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        return render(request,"payment/not_shipped_dash.html",{'orders':orders})
    else:
        messages.success(request, "Order Denied")
        return redirect('home')

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        return render(request,"payment/shipped_dash.html",{'orders':orders})
    else:
        messages.success(request, "Order Denied")
        return redirect('home')
    
def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        # Get Billing info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get shipping session data
        my_shipping = request.session.get('my_shipping')
        # Gather Order info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # Create Shipping Address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        # Create an Order
        if request.user.is_authenticated:
            user = request.user
            # Create order
            create_order = Order(user=user,full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
            create_order.save()

            # Add order items
            # Get the order ID
            order_id = create_order.pk
            # Get product ID
            for product in cart_products():
                product_id = product.id
                # Get product price
                if product.is_sale:
                    procie = product.sale_price
                else:
                    price = product.price
                # Get quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()

             # del our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]



            messages.success(request,"Order Placed")
            return redirect('home')
        else:
            # not logged in
            create_order = Order(full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
            create_order.save()

            # Add order items
            # Get the order ID
            order_id = create_order.pk
            # Get product ID
            for product in cart_products():
                product_id = product.id
                # Get product price
                if product.is_sale:
                    procie = product.sale_price
                else:
                    price = product.price
                # Get quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()

            # del our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]


            messages.success(request,"Order Placed")
            return redirect('home')

    else:
        messages.success(request,"Access Denied")
        return redirect('home')


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Create a session with Shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # เช็คว่าผูัใช้เข้าสู่ระบบหรือยัง
        if request.user.is_authenticated:
             # Get the Billing Form
             billing_form = PaymentForm()
             return render(request, 'payment/billing_info.html',{
                'cart_products':cart_products,
                'quantities':quantities,
                'totals':totals,
                'shipping_info':request.POST,
                'billing_form':billing_form,})
        else:
            # ไม่ได้ล็อกอิน
        #    if request.user.is_authenticated:
            # Get the Billing Form
             billing_form = PaymentForm()
             return render(request, 'payment/billing_info.html',{
                'cart_products':cart_products,
                'quantities':quantities,
                'totals':totals,
                'shipping_info':request.POST,
                'billing_form':billing_form,})

        shipping_form = request.POST
        return render(request, 'payment/billing_info.html',{
            'cart_products':cart_products,
            'quantities':quantities,
            'totals':totals,
            'shipping_form':shipping_form})
    else:
        messages.success(request,"Access Denied")
        return redirect('home')


def payment_success(request):
    return render(request, 'payment/payment_success.html',{})


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    if request.user.is_authenticated:
        # เช็คเอ้าโดยล็อคอิน user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html',{
        'cart_products':cart_products,
        'quantities':quantities,
        'totals':totals,
        'shipping_form':shipping_form})
    else:
        # เช็คเอ้าโดยไม่ได้ login
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html',{
        'cart_products':cart_products,
        'quantities':quantities,
        'totals':totals,
        'shipping_form':shipping_form})
