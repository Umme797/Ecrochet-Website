from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from ecrochetapp.models import Product, Cart, Order, Pattern, Payment
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import logging
from django.shortcuts import render, get_object_or_404



def index(request):
    context = {}
    p = Product.objects.filter(is_active=True)
    context['products'] = p
    return render(request, 'index.html', context)



def pdetails(request, pid):
    p = Product.objects.filter(id=pid)
    context={}
    context['products'] = p
    return render(request,'productdetails.html',context)



def addtocart(request, pid):
    if request.user.is_authenticated:
        userid = request.user.id
        u = User.objects.filter(id = userid)
        p = Product.objects.filter(id = pid)

        q1 = Q(uid=u[0])
        q2 = Q(pid=p[0])
        c = Cart.objects.filter(q1 & q2)

        context = {}
        context["products"] = p

        n = len(c)
        if n==1:
            context['errmsg'] = "Product Already Exists in the Cart."
        else:
            c = Cart.objects.create(uid=u[0], pid=p[0])
            c.save()
            context["success"] = "Product Added to the Cart."
        return render(request, 'productdetails.html', context)
    else:
        return redirect("/login")



def viewcart(request, context=None):
    c = Cart.objects.filter(uid=request.user.id)
    s = 0
    for x in c:
        s += x.pid.price * x.qty
    if context is None:
        context = {}
    context['data'] = c
    context['total'] = s
    return render(request, 'viewcart.html', context)



def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')



def updateqty(request, qv, cid):
    c = Cart.objects.filter(id=cid)
    if not c.exists():
        return redirect('/viewcart')  
    item = c[0]
    MAX_QUANTITY = 10  
    context = {}
    if qv == '1':  
        if item.qty < MAX_QUANTITY:  
            item.qty += 1
            item.save()
        else:
            context['maxqty'] = f"You cannot add more than {MAX_QUANTITY} items."
    else: 
        if item.qty > 1:  
            item.qty -= 1
            item.save()
    return viewcart(request, context)



def register(request):
    if request.method == 'POST':
        uname = request.POST.get('uname', '').strip()
        email = request.POST.get('email', '').strip()
        upass = request.POST.get('upass', '').strip()
        context = {}
        if uname=="" or email=="" or upass=="":
            context['errmsg'] = "Please fill all the fields"
            return render(request, 'register.html', context)
        else:
            try:
                u = User.objects.create(password = upass, username = uname, email = email)
                u.set_password(upass)
                u.save()
                context['succmsg'] = "User  Registered Successfully"
                return render(request, 'register.html', context)
            except Exception as e:
                print("Error:", e)
                context['errmsg'] = "User  already exists. Use another Email ID"
                return render(request, 'register.html', context)
    else:
        return render(request, 'register.html')



def ulogin(request):
    if request.user.is_authenticated:
        return redirect("/index")  
    if request.method == "POST":
        uname = request.POST.get('uname', '').strip()
        upass = request.POST.get('upass', '').strip()
        context = {}        
        if not uname or not upass:
            context['errmsg'] = "Please fill all the fields"
            return render(request, 'ulogin.html', context)
        else:
            u = authenticate(username=uname, password=upass)
            if u is not None:
                login(request, u)
                return redirect("/index")
            else:
                context['errmsg'] = "Invalid Username/Password!!"
                return render(request, 'ulogin.html', context)
    else:
        return render(request, 'ulogin.html')



def ulogout(request):
    logout(request)
    return redirect('/index')



def patterns(request):
    context = {}
    p = Pattern.objects.all()
    context['patterns'] = p
    return render(request, 'patterns.html', context)



def pattern_details(request, pid):
    pattern = get_object_or_404(Pattern, id=pid)
    print("Pattern Retrieved:", pattern)
    return render(request, 'pattern_details.html', {'pattern': pattern})



def search_patterns(request):
    context = {}
    query = request.GET.get('q')
    context["patterns"] = Pattern.objects.filter(name__icontains=query)
    return render(request, 'patterns.html', context)



def placeorder(request):
    context = {}  
    if request.method == "POST":
        c = Cart.objects.filter(uid=request.user.id)
        oid = random.randrange(1, 1000)
        for x in c:
            o = Order.objects.create(order_id=oid, pid=x.pid, uid=x.uid, qty=x.qty)
            o.save()

        shipadd = request.POST.get("shipadd")
        paymentmethod = request.POST.get("payment")

        if not shipadd or not paymentmethod:
            context['errmsg'] = 'Please fill out all fields before placing the order.'
            return render(request, 'placeorder.html', context)

        orders = Order.objects.filter(uid=request.user.id)
        total_amount = 0  
        for x in orders:
            s = x.pid.price * x.qty  
            total_amount += s  

        if total_amount <= 0:
            context['errmsg'] = 'Your cart is empty. Please add items before placing an order.'
            return render(request, 'placeorder.html', context)

        payment_record = Payment.objects.create(
            uid=request.user,
            address=shipadd,
            payment=paymentmethod,
            total=total_amount
        )

        client = razorpay.Client(auth=("rzp_test_piZcOeJlTxPhS3", "jogS2NzDBUe3z8FjZpZbKyXg"))
        data = {"amount": int(total_amount * 100), "currency": "INR", "receipt": str(payment_record.id)}
        
        try:
            payment_response = client.order.create(data=data)
            context['successmsg'] = 'Order placed successfully! Proceed to payment.'
            context['payment_response'] = payment_response
            return render(request, 'pay.html', context)
        except razorpay.errors.BadRequestError as e:
            context['errmsg'] = f"Payment failed to initiate: {str(e)}"
            return render(request, 'placeorder.html', context)
        
    return render(request, 'placeorder.html', context)



def makepayment(request):
    orders = Order.objects.filter(uid=request.user.id)
    np = len(orders)
    s = 0
    for x in orders:
        s = s + x.pid.price * x.qty
        oid = x.order_id
    client = razorpay.Client(
        auth=("rzp_test_piZcOeJlTxPhS3", "jogS2NzDBUe3z8FjZpZbKyXg")
    )
    data = {"amount": s * 100, "currency": "INR", "receipt": oid}
    payment = client.order.create(data=data)
    return render(request, 'pay.html')



logger = logging.getLogger(__name__)
def sendusermail(request):
    user = request.user
    orders = Order.objects.filter(uid=user.id)

    if not orders.exists():
        logger.warning(f"No orders found for user: {user.username}")
        return redirect('index')

    order_items = []
    total_amount = 0  
    for order in orders:
        order_items.append({'product_name': order.pid.name, 'quantity': order.qty})
        total_amount += order.pid.price * order.qty  

    total = total_amount
    subject = "Order Confirmation"
    from_email = "umme2509zr@example.com"
    recipient_list = [user.email]

    if not user.email:
        logger.error(f"User  {user.username} does not have a valid email address.")
        return redirect('index')

    html_content = render_to_string('order_confirmation_email.html', {
        'user': user,
        'order_items': order_items,
        'total': total,
    })

    text_content = f"Hi {user.username},\n\nThank you for your order!\n\nOrder Details:\n"
    for item in order_items:
        text_content += f"- {item['product_name']} (Quantity: {item['quantity']})\n"
    text_content += f"\nTotal Amount: ${total:.2f}\n\nThank you for shopping with us!"

    email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    email.attach_alternative(html_content, "text/html")

    try:
        email.send()
        logger.info(f"Order confirmation email sent to {user.email}.")
    except Exception as e:
        logger.error(f"Error sending email to {user.email}: {e}")

    return render(request, 'index.html')



def search(request):
    query = request.GET.get('q', '')  
    context = {}
    
    if query:  
        context['products'] = Product.objects.filter(name__icontains=query)
        context['no_products'] = not context['products']  
        print(f"Query: {query}, Products found: {context['products']}, No products: {context['no_products']}")
    else:
        context['products'] = Product.objects.all()
        context['no_products'] = False  

    return render(request, 'index.html', context)

