from django.shortcuts import render,redirect
#from django.contrib.auth import authenticate, login
#from django.contrib.auth import logout
from django.contrib.auth.models import User,auth
from django.contrib import messages
from dmezapp.models import Product, Products,newregis, Customer, Order, OrderItem, ShippingAddress
from math import ceil
from django.http import JsonResponse
import datetime
from .utils import cookieCart, cartData, guestOrder
import json

# Create your views here.

def home(request):
	return render(request,'index.html')

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'allproduct.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'cart.html', context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'checkout.html', context)



def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)







def allproduct(request):
    allProds = []
    catprods = Products.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Products.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'allproduct.html', params)

def productView(request, myid):

    # Fetch the product using the id
    products = Product.objects.filter(id=myid)
    return render(request, 'product.html', {'products':products[0]})


def about(request):
	return render(request,'about.html')

def contact(request):
	return render(request,'contact.html')

def testing(request):
	return render(request,'testing.html')

def join(request):
	return render(request,'join.html')

def upload(request):
	return render(request,'upload.html')

def top(request):
	return render(request,'top.html')

def specific(request):
	return render(request,'specificpage.html')

def bestselling(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request,'bestsellingproduct.html', context)

def account(request):
	return render(request,'account.html')

def consult(request):
	return render(request,'consult.html')



########################Account Section#############################

def signup(request):
	if request.method=='POST':
		username = request.POST['username']
		email = request.POST['email']
		password1 = request.POST['password1']
		password11 = request.POST['password11']
		if password1==password11:
			if User.objects.filter(username=username).exists():
				messages.info(request,'Username Taken')
				return redirect('/account')
			elif User.objects.filter(email=email).exists():
				messages.info(request,'Email Taken')
				return redirect('/account')
			else:
				user=User.objects.create_user(username=username, password=password1, email=email)
				user.save();
				auth.login(request,user)
				print('user created')
		else:
			messages.info(request,'Password not Matching')
			return redirect('/account')
		return redirect('/')


	else:
		return render(request,'account.html')


def login(request):
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']
		user=auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request,user)
			return redirect('/') 
		else:
			return redirect('/account') 
	else:
		return render(request,'account.html')

def logout(request):
	auth.logout(request)
	return redirect('/')

