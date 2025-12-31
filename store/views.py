from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views import View

from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.cart import Cart
from .models.order import OrderDetail

from django.db.models import Q
from django.http import JsonResponse
# Create your views here.

def home(request):
    totalitem = 0
    name=""
    if request.session.has_key('phone'):
        phone = request.session["phone"]

        category = Category.get_all_categories()
        customer = Customer.objects.filter(phone=phone)
        totalitem = len(Cart.objects.filter(phone=phone))

        categoryID = request.GET.get('category')

        if categoryID:
            products = Product.get_all_product_by_category_id(categoryID)
        else:
            products = Product.get_all_products()

        for c in customer:
            name = c.name

        data = {
            'name': name,
            'product': products,
            'category': category,
            'totalitem': totalitem
        }

        return render(request, 'home.html', data)

    else:
        return redirect('login')

        
class Signup(View):
    def get(self,request):
       return render(request, 'signup.html')
    def post(self,request):
        postData=request.POST
        name=postData.get('name')
        phone=postData.get('phone')
        email=postData.get('email')

        error_message = None

        value={
            'phone':phone,
            'name':name,
            'email':email
        }
        customer=Customer(name=name,
                          phone=phone,
                          email=email)
        
        if(not name):
            error_message="Name is required"
        elif(not phone):
            error_message="Mobile Number is required"
        elif(len(phone)<10 or len(phone))>10:
            error_message="Mobile number must consists of 10 numbers"
        elif customer.isExist():
            error_message="Mobile number already exist"
        elif(not email):
            error_message="Email is required"
        

        if not error_message:
            messages.success(request,'Registered Sucessfully!!!')
            customer.register()
            return redirect('signup')
        else:
            data={
                'error':error_message,
                'value':value
            }
            return render(request,'signup.html',data)

class Login(View):
    def get(self,request):
        return render(request, 'login.html')
    def post(self,request):
        phone=request.POST.get('phone')
        error_message=None
        value={'phone':phone}
        customer=Customer.objects.filter(phone=request.POST["phone"])
        if customer:
            request.session['phone']=phone
            return redirect("homepage")
        else:
            error_message="Mobile number is invalid!!!"
            data={'error':error_message,
                  'value':value}

        return render(request,'login.html',data)
    
def productdetail(request,pk):
    totalitem=0
    product=Product.objects.get(pk=pk)
    item_already_in_cart=False
    if request.session.has_key('phone'):
        phone=request.session['phone']
        totalitem=len(Cart.objects.filter(phone=phone))
        item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(phone=phone)).exists()
        customer=Customer.objects.filter(phone=phone)
        for c in customer:
            name=c.name
        data={'product':product,
              'item_already_in_cart':item_already_in_cart,
              'name':name,
              'totalitem':totalitem}

        return render(request,'productdetail.html', data)
    else:
        return redirect('login')


def logout(request):
    if request.session.has_key('phone'):
        del request.session["phone"]
        return redirect('login')
    else:
        return redirect('login')
    
def add_to_cart(request):
    phone=request.session['phone']
    product_id=request.GET.get('prod_id')
    product_name=Product.objects.get(id=product_id)
    product=Product.objects.filter(id=product_id)
    for p in product:
        image=p.image
        price=p.price
        Cart(phone=phone,product=product_name,image=image,price=price).save()
        return redirect(f"/product-detail/{product_id}")
    

def show_cart(request):
    if request.session.has_key('phone'):
        phone = request.session['phone']

        totalitem = Cart.objects.filter(phone=phone).count()
        cart = Cart.objects.filter(phone=phone)  

        customer = Customer.objects.filter(phone=phone)
        name = ""
        for c in customer:
            name = c.name

        data = {
            'name': name,
            'cart': cart,
            'totalitem': totalitem
        }

        if cart:
            return render(request, 'show_cart.html', data)
        else:
            return render(request,'empty_cart.html',data)
    else:
        return redirect('login')




def plus_cart(request,product_id,op):
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        print(product_id)
        cart = Cart.objects.get(Q(product=product_id) & Q(phone=phone))
        if op == '-':
            if cart.quantity > 0:
                cart.quantity -= 1
                cart.save()
        else:
            
                cart.quantity += 1
                cart.save()
            
        return redirect('show_cart')
from django.http import JsonResponse
from django.db.models import Q
from .models import Cart

def remove_cart(request):
    if not request.session.get('phone'):
        return JsonResponse({'status': 'fail', 'message': 'User not logged in'})

    phone = request.session['phone']
    prod_id = request.GET.get('prod_id')

    # Remove product from cart
    Cart.objects.filter(
        Q(product__id=prod_id) & Q(phone=phone)
    ).delete()

    # Check cart status
    cart_count = Cart.objects.filter(phone=phone).count()

    if cart_count == 0:
        return JsonResponse({
            'status': 'empty',
            'cart_count': 0
        })

    return JsonResponse({
        'status': 'success',
        'cart_count': cart_count
    })



def offers(request):
    offer_products = Product.objects.filter(category__name="Offer")

    data = {
        'products': offer_products
    }

    if request.session.has_key('phone'):
        phone = request.session['phone']

        totalitem = Cart.objects.filter(phone=phone).count()
        cart = Cart.objects.filter(phone=phone)

        customer = Customer.objects.filter(phone=phone)
        name = ""
        for c in customer:
            name = c.name

        # add cart-related data
        data.update({
            'name': name,
            'cart': cart,
            'totalitem': totalitem
        })

        return render(request, "offers.html", data)
    else:
        return redirect('login')

def checkout(request): 
    totalitem=0 
    if request.session.has_key('phone'): 
        phone = request.session["phone"] 
        name=request.POST.get('name') 
        address=request.POST.get('address') 
        mobile=request.POST.get('mobile') 
        cart_product=Cart.objects.filter(phone=phone) 
        for c in cart_product: 
            quantity=c.quantity 
            price=c.price 
            product_name=c.product 
            image=c.image 
            OrderDetail(user=phone,product_name=product_name,image=image,quantity=quantity,price=price).save() 
            cart_product.delete() 
            totalitem=len(Cart.objects.filter(phone=phone)) 
            customer = Customer.objects.filter(phone=phone) 
            for c in customer: name=c.name 
            data={ 'name':name, 
                  'totalitem':totalitem, 
                  'success_message': "🐟 Your order has been successfully placed! Thank you for shopping with us." 
                  } 
        return render(request,'empty_cart.html',data) 
    else: 
        return redirect('login')
    

def order(request):
    totalitem=0
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        totalitem=len(Cart.objects.filter(phone=phone))
        customer = Customer.objects.filter(phone=phone)
        for c in customer:
            name=c.name
            order=OrderDetail.objects.filter(user=phone)
            data={
            'order':order,
            'name':name,
            'totalitem':totalitem
            }
           
            if order:
                return render (request,'order.html',data)
            else:
                return render(request, 'emptyorder.html',data)
    
    else:
        return redirect('login')
    
def search(request):
    totalitem=0
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        query=request.GET.get('query')
        search=Product.objects.filter(name__icontains=query)
        category=Category.get_all_categories()
        totalitem=len(Cart.objects.filter(phone=phone))
        customer = Customer.objects.filter(phone=phone)
        for c in customer:
            name=c.name
        data={
                'name':name,
                'totalitem':totalitem,
                'search':search,
                'category':category,
                'query':query
            }
        return render(request,'search.html',data)
    else:
        return redirect('login')
    
def clear_orders(request):
    if request.session.has_key('phone'):
        phone = request.session["phone"]
        OrderDetail.objects.filter(user=phone).delete()
    return redirect('order') 
