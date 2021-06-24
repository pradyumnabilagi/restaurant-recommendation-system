from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.decorators import login_required



def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'capp/register.html', context)


def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'capp/login.html', context)




def logoutUser(request):
	logout(request)
	return redirect('login')
@login_required(login_url='login')
def home(request):

    allorders=order.objects.filter(user=request.user)
    allrestaurants=restaurant.objects.filter()
    freq={}
    for Order in allorders:
        if Order.restaurants in set(freq.keys()):
            freq[Order.restaurants]+=1
        else:
            freq[Order.restaurants]=1
    if len(list(freq.keys())) ==0 or len(list(freq.keys()))==1:
        context={'user' : request.user,'restaurants':allrestaurants,'msg':"Choose restaurants"}
    else:
        max=0
        restaurants=[]
        for res in list(freq.keys()):
            if max<freq[res]:
                max=freq[res]
        for res in list(freq.keys()):
            if max==freq[res]:
                restaurants.append(res)
        if len(restaurants)==len(allrestaurants):
            restaurants.pop(0)
        context = {'user': request.user, 'restaurants': restaurants,'msg':"Recomended restaurants"}


    return render(request,'capp/dashboard.html',context)


@login_required(login_url='login')
def menu1(request,pk):
    rest = restaurant.objects.get(id=pk)
    menus= menu.objects.filter(restaurants=rest)
    context={'menus':menus,'rest':rest}
    return render(request,'capp/menu.html',context)
a=" " 

@login_required(login_url='login')
def addtocart(request, itemid):
    if request.user.is_anonymous :
        return redirect('login')
    user = request.user
    quentity = request.POST['quantity']
    menus = menu.objects.get(id=itemid)
    carts = cart.objects.filter(user=request.user)
    b = carts.count()
    print(b)
    if float(quentity) < 1.0:
        messages.add_message(request, messages.INFO, 'Minimum quantity should be 1')
        return redirect('home')
    k=int(0)


    menus.quantity = quentity
    menus.amount = float(quentity) * menus.price

    menus.save()
    m = menus.restaurants.resname
    if b == 0:
        cart1 = cart(user=user, menu=menus)
        cart1.save()

    elif  str(carts[0].menu.restaurants.resname) == str(m) and b != 0:
        for l in range(len(carts)):
            if carts[l].menu.id == menus.id:
                menus.quantity += int(quentity)
                menus.amount = float(menus.quantity) * menus.price
                menus.save()
                return redirect(request.META['HTTP_REFERER'])
        cart1 = cart(user=user, menu=menus)
        cart1.save()

    else:
        messages.add_message(request, messages.INFO, 'You cannot place order from different restaurants')

        return redirect('home')

    print(cart1.menu.quantity)
    return redirect(request.META['HTTP_REFERER'])
c=0.0

r=0.0
y=0.0
j=0.0
@login_required(login_url='login')
def cartview(request):
    global c
    global r
    global y
    global j
    cartitems = cart.objects.filter(user=request.user)



    c=0.0
    r=0.0
    j=0.0
    for i in cartitems:
        
        c += i.menu.amount 
        
        if i.menu.duration > r:
            r=i.menu.duration
        
        j=j+1        



    if j==0:
        y=0.0
    else:
        y=r+15.0          
    return render(request,"capp/cart.html",{'cartitems' : cartitems,'c':c,'r':r,'y':y})


@login_required(login_url='login')
def deletefromcart(request,cartid):
    global c
    cart.objects.get(id = cartid).delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login')
def placeorder(request):
    if len(cart.objects.filter(user=request.user))==0 :
        return redirect('home')
    global c
    menus = [" x ".join([z.menu.dname,str(z.menu.quantity)]) for z in cart.objects.filter(user = request.user)]
    for i in cart.objects.filter(user=request.user):
        name=i.menu.restaurants
    c=0.0
    for i in cart.objects.filter(user=request.user):
        
        c += i.menu.amount     

    order(user = request.user,items= "\n".join(menus),restaurants=name,total=c).save()

    messages.add_message(request,messages.INFO,'Your order is succesfully placed')
    for i in cart.objects.filter(user = request.user):
        i.delete()
    c=0.0
    return redirect('home')


@login_required(login_url='login')
def ordersview(request):
    orders = []
    for i in order.objects.filter(user = request.user):
        orders.append(i)
    context = {'orders' : orders}
    return render(request,"capp/orders.html",context)

@login_required(login_url='login')
def searchview(request):
    search = request.POST['search']

    restaurants = [res for res in restaurant.objects.all() if str.lower(res.resname).find(str.lower(search))!=-1]
    vari=set({})
    if len(restaurants)==0 :
        menus= [menu for menu in menu.objects.all() if str.lower(menu.dname).find(str.lower(search))!=-1]
        for i in range(0,len(menus)):
            vari=vari.union(set({menus[i].restaurants}))
        restaurants=list(vari)

    if len(restaurants)==0:
        context={'restaurants':restaurants,'alertmess':"could not find any restaurants!!!"}
    else:
        context = {'restaurants':restaurants,'alertmess':""}
    return render(request,"capp/dashboard.html",context)



    




	