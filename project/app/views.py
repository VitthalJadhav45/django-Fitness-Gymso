from django.shortcuts import render,redirect,HttpResponse
from .models import Registration,Query
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import razorpay
from project.settings import RAZOPAY_API_KEY, RAZOPAY_API_SECRET_KEY
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='login')
def home(request):
    return render(request,'index.html')

@csrf_exempt
def about(request):
    return render(request,'about.html')

def trainer(request):
    return render(request,'trainer.html')

def classes(rerquest):
    return render(rerquest,'classes.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        en=Query(name=name,email=email,message=message)
        en.save()
    return render(request,'contact.html')

def signupPage(request):
    if request.method == 'POST':
       uname=request.POST.get('username')
       email=request.POST.get('email')
       pass1=request.POST.get('pass1')
       pass2=request.POST.get('pass2')

       if pass1!=pass2:
           return HttpResponse("Pass1 is not matched pass2 ")
       else:
           my_user=User.objects.create_user(uname,email,pass1)    
           return redirect('login')
    
    return render(request,'signup.html')

def LoginPage(request):
    if request.method == 'POST':
        uname=request.POST.get('username')
        pass1=request.POST.get('pass1')
        user=authenticate(request,username=uname,password=pass1)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("username or password wrong")
        
    return render(request,'login.html')



client = razorpay.Client(auth=(RAZOPAY_API_KEY, RAZOPAY_API_SECRET_KEY))
def payment(request):
    if request.method == 'POST':
       name=request.POST.get('username')
       email=request.POST.get('email')
       age=request.POST.get('age')
       phone=request.POST.get('phone')   

       order_amount = 50000
       order_currency = "INR"
       payment_order=client.order.create(dict(amount=order_amount,currency=order_currency,payment_capture=1))   
       payment_order_id=payment_order['id']
       order_status = payment_order['status']

       if order_status == 'created':
        en = Registration(
            name=name,
            email=email,
            age=age,
            phone=phone,
            amount=order_amount,
            order_id=payment_order_id,
            paid = True
        )
        en.save()
        
        context={
           'amount':50000, 
           'api_key':RAZOPAY_API_KEY,
           'order_id':payment_order_id
        }
        return render(request,'payment.html',context)
       
    return render(request,'payment.html')
    
    