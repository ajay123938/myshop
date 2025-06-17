from django.shortcuts import render,redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse,JsonResponse
import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
logger = logging.getLogger(__name__)
import hashlib
import hmac


# Create your views here.


def  cateogry(request,str):
 if request.method == "POST":
    if str == 'men':
      men_objs = Product.objects.filter(cateogry=str)
      men_objs=  men_objs.filter(name__icontains = request.POST.get('search'))
      print(request.POST.get('search'))
      context = {'objs':men_objs}

    elif str == 'women':
      women_objs = Product.objects.filter(cateogry=str)
      women_objs=  women_objs.filter(name__icontains = request.POST.get('search'))
      context = {'objs':women_objs}

    elif str == 'kids':
      kids_objs = Product.objects.filter(cateogry=str)
      kids_objs=  kids_objs.filter(name__icontains = request.POST.get('search'))
      context = {'objs':kids_objs}
    else:
        
       all_product = Product.objects.all()
       all_product=  all_product.filter(name__icontains = request.POST.get('search'))
       context = {'objs':all_product}

 else:
    if str == 'men':
      men_objs = Product.objects.filter(cateogry=str)
      context = {'objs':men_objs}

    elif str == 'women':
      women_objs = Product.objects.filter(cateogry=str)
      context = {'objs':women_objs}
   
    elif str == 'kids':
      kids_objs = Product.objects.filter(cateogry=str)
      context = {'objs':kids_objs}
    
    else:
       all_product = Product.objects.all()
       context = {'objs':all_product}

 
 return render(request,'product/index.html',context)



def login1(request):
    if request.method == "POST":
      username  = request.POST.get('username')
      password = request.POST.get('password')

      if User.objects.filter(username = username).exists():
      
         user = authenticate(request,username = username,password=password)
         if user is not None:
            login(request,user)
            return  redirect('/cart/')
         else:
             return redirect('/login/')
      
  
    return render(request,'account/login.html')
   
@login_required
@csrf_exempt
def order(request):
    if request.method == 'POST':
        try:
            # Log the request body
            logger.debug(f"Request body: {request.body}")

            # Ensure the request body is not empty
            if not request.body:
                return JsonResponse({'status': 'error', 'message': 'Empty request body'}, status=400)
            
            # Parse JSON data
            data = json.loads(request.body)
            logger.debug(f"Parsed data: {data}")

            # Get cart data, default to an empty dict if 'cart' key is missing
            cart = data.get('cart', None)
            if cart is None:
                return JsonResponse({'status': 'error', 'message': 'Cart data is missing'}, status=400)
            
            logger.debug(f"Cart data: {cart}")
            print(cart)

            for key, value in cart.items():
              product = Product.objects.filter(id=key)
              if value[0] !=0:
                 Order.objects.create(user=request.user,product = product[0],qty=value[0])
            
            
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    # Return an error response for non-POST requests
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
@login_required
def your_order(request):
    order_objs = Order.objects.filter(user=request.user)
    if order_objs.exists():
       for i in order_objs:
          if  i.user_received == True:
            i.delete()
       
    context = {'order_objs':order_objs}
    return render(request,'order/order.html',context)

  
def register(request):
   if request.method == "POST":
     first_name  =  request.POST.get('first_name')
     last_name=     request.POST.get('last_name')
     email = request.POST.get('username')
     password =request.POST.get('password')
     user_objs = User.objects.create(first_name = first_name,last_name=last_name,username=email)
     user_objs.set_password(password)
     user_objs.save()
     return redirect('/cateogry/product')
   return render(request,'account/register.html')

def cart(request):
    if request.user.is_authenticated:
       return render(request,'cart/cart.html')
    else:
     return redirect('login1')
   
def custom_logout_view(request):
    logout(request)
    return redirect('/cateogry/product') 


