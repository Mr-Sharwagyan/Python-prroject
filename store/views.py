from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views import View

from .models.product import Product
from .models.category import Category
from .models.customer import Customer
# Create your views here.

def home(request):
    products= None
    category=Category.get_all_categories()

    categoryID=request.GET.get('category')
    if categoryID:
        products=Product.get_all_product_by_category_id(categoryID)
    else:
        products = Product.get_all_products()

    data={}
    data['product']=products
    data['category']=category

    return render(request,'home.html',data)
       
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
        elif(len(phone))<10:
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
            return redirect("homepage")
        else:
            error_message="Mobile number is invalid!!!"
            data={'error':error_message,
                  'value':value}

        return render(request,'login.html',data)
    
def productdetail(request,pk):
    product=Product.objects.get(pk=pk)
    return render(request,'productdetail.html', {'product':product})