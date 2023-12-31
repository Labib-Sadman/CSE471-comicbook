from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Productdata,Cart,OrderPlaced,ProductImage
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



#####
from django.contrib.auth import views as auth_views
from django.urls import reverse

class CustomLoginView(auth_views.LoginView):

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse('admin:index')
        return super().get_success_url()

#####




class ProductView(View):
    def get(self,request):
      totalitem=0  
      superhero=Productdata.objects.filter(category='S')  
      nonfiction=Productdata.objects.filter(category='NF')  
      sciencefiction=Productdata.objects.filter(category='SF')  
      horror=Productdata.objects.filter(category='H')
      if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user)) 
      return render(request,'app/home.html',{"superhero":superhero,"nonfiction":nonfiction,"sciecefiction":sciencefiction,"horror":horror,"totalitem":totalitem})
  


class ProductDetailView(View):
    def get(self,request,pk):
        totalitem=0
        product=Productdata.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        productlist = ProductImage.objects.filter(product=pk)
        if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user)) 
        return render(request,'app/productdetail.html',{'product':product,'totalitem':totalitem,'productlist':productlist,"item_already_in_cart":item_already_in_cart})
    
from django.shortcuts import get_object_or_404


@login_required
def add_to_cart(request):
    user = request.user
    product_id = int(request.GET.get('prod_id'))
    product = get_object_or_404(Productdata, id=product_id)
    cart = Cart(user=user, product=product)
    cart.save()
    messages.success(request, 'Product added to cart successfully.')
    return redirect('/cart', {'added_to_cart': True})

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discounted_price)
                amount+=tempamount
            total_amount=amount+shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart,"totalamount":total_amount,'amount':amount})
        else:
            return render(request,'app/emptycart.html')


def plus_cart(request):
  if request.method=="GET":
    prod_id=request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    amount=0.0
    shipping_amount=70.0
    cart_product= [p for p in Cart.objects.all() if p.user==request.user]
    for p in cart_product:
        tempamount = (p. quantity * p.product. discounted_price)
        amount += tempamount
    data= {
      'quantity' :c.quantity,
      'amount': amount,
      'totalamount': amount + shipping_amount
        }
    return JsonResponse(data)

def minus_cart(request):
  if request.method=="GET":
    prod_id=request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity-=1
    c.save()
    amount=0.0
    shipping_amount=70.0
    cart_product= [p for p in Cart.objects.all() if p.user==request.user]
    for p in cart_product:
        tempamount = (p. quantity * p.product. discounted_price)
        amount += tempamount
    data= {
      'quantity' :c.quantity,
      'amount': amount,
      'totalamount': amount + shipping_amount
        }
    return JsonResponse(data)


def remove_cart(request):
  if request.method=="GET":
    prod_id=request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    amount=0.0
    shipping_amount=70.0
    cart_product= [p for p in Cart.objects.all() if p.user==request.user]
    for p in cart_product:
        tempamount = (p. quantity * p.product. discounted_price)
        amount += tempamount
    data= {
      'amount': amount,
      'totalamount': amount + shipping_amount
        }
    return JsonResponse(data)



def buy_now(request):
 return render(request, 'app/buynow.html')

def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',{"add":add,'acitive':'btn-primary'})

@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

def product_search(request):
    query = request.GET.get('q')  # Get the search query from the URL parameter 'q'

    if query:
        products = Productdata.objects.filter(title__icontains=query)
    else:
        products = Productdata.objects.all()

    return render(request, 'app/product_search_results.html', {'products': products})

def superheros(request,data=None):
    if data==None:
        superheros=Productdata.objects.filter(category="S")
    elif data=="DC" or data=="Marvel":
        superheros=Productdata.objects.filter(category="S").filter(brand=data)
    return render(request, 'app/superheros.html',{'superheros':superheros})

def nonfiction(request,data=None):
    if data==None:
        nonfiction=Productdata.objects.filter(category="NF")
    elif data=="Manga":
        nonfiction=Productdata.objects.filter(category="NF").filter(brand=data)
    return render(request, 'app/nonfiction.html',{'nonfiction':nonfiction})

def aboutus(request):
    return render(request,'app/aboutus.html')


def sciencefiction(request,data=None):
    if data==None:
        sciencefiction=Productdata.objects.filter(category="SF")
    elif data=="LSA publications":
        sciencefiction=Productdata.objects.filter(category="SF").filter(brand=data)
    return render(request, 'app/sciencefiction.html',{'sciencefiction':sciencefiction})

def horror(request,data=None):
    if data==None:
        horror=Productdata.objects.filter(category="H")
    elif data=="Ash publications":
        horror=Productdata.objects.filter(category="H").filter(brand=data)
    return render(request, 'app/horror.html',{'horror':horror})

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{"form":form})
    def post(self,request):
        form=form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,"Congratulation! Registered Successfully")
            form.save()
        return render(request, 'app/customerregistration.html',{"form":form})
@login_required
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    totalamount=0.0
    cart_product= [p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p. quantity * p.product. discounted_price)
            amount += tempamount
        totalamount=amount+shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,"cart_items":cart_items})
@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('orders')
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulation!! Profile Updated Successfully")
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})