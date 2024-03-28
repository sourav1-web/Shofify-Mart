from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Cart,Product,OrderPlaced
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import CustomerProfileForm
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Sum
from django.http import JsonResponse


class HomeView(View):
    def get(self, request):
        mobile = Product.objects.filter(catagory="M")
        laptops = Product.objects.filter(catagory="L")
        bottom_wear = Product.objects.filter(catagory="BW")
        top_wear = Product.objects.filter(catagory="TW")
        ladies_bottomwear = Product.objects.filter(catagory="LB")
        ladies_topwear = Product.objects.filter(catagory="LS") 

        user = request.user if request.user.is_authenticated else None
        total_quantity = 0

        if user:
            cart_quantity = Cart.objects.filter(user=user)
            total_quantity = cart_quantity.aggregate(total_quantity=Sum('quantity'))['total_quantity']

        context = {
            'mobile': mobile,
            'bottom_wear': bottom_wear,
            'top_wear': top_wear,
            'laptops': laptops,
            'ladies_bottomwear': ladies_bottomwear,
            'ladies_topwear': ladies_topwear, 
            'total_quantity': total_quantity, 
        }
        return render(request, 'app/home.html', context=context)



class Product_detailView(View):
 def get(self,request,pk):
  product=Product.objects.get(pk=pk)
  return render(request,'app/productdetail.html',{'product':product}) 

@login_required
def add_to_cart(request):
 user=request.user
 product_id=request.GET.get('prd_id')
 product=Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('showcart')

def showCart(request):
   if request.user.is_authenticated:
      user=request.user
      carts=Cart.objects.filter(user=user)
     
      amount=0.0
      shipping_amount=70
      tot_amount=0.0
      cart_product=[p for p in Cart.objects.all() if p.user==user]
      if cart_product:
         for p in cart_product:
            temp_amount=(p.quantity * p.product.discount_price)
            amount +=temp_amount
            tot_amount=amount+shipping_amount
      return render(request,'app/addtocart.html',{'carts':carts,'total_amount':tot_amount,'amount':amount})




def buy_now(request):
 return render(request, 'app/buynow.html')





def address(request):
    # Filter addresses based on the logged-in user
    addresses = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'addresses': addresses, 'active': 'btn-primary'})


def orders(request):
 op=OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'order_placed':op})

@login_required
def mobile(request,data=None):
 if data ==None:
  mobiles=Product.objects.filter(catagory='M')
 elif data=="samsung" or data=="mi":
  mobiles=Product.objects.filter(catagory='M').filter(brand=data)
 return render(request, 'app/mobile.html',{'mobiles':mobiles})

def Laptop(request,data=None):
 if data == None:
  laptops=Product.objects.filter(catagory='L')
 elif data=="hp" or data=="dell":
  laptops=Product.objects.filter(catagory='L').filter(brand=data) 
 return render(request,'app/laptop.html',{'laptops':laptops})

def Bottomwear(request,data=None):
    if data == None:
        bottomwears=Product.objects.filter(Q(catagory='BW') | Q(catagory="LB"))
    elif data=="ladies":
        bottomwears=Product.objects.filter(catagory="LB")
 
    return render(request,'app/bottomwear.html',{'bottomwears':bottomwears})



def topwear(request,data=None):
 if data == None:
  topwears = Product.objects.filter(Q(catagory='LS') | Q(catagory='TW'))
 elif data=="ladies":
  topwears=Product.objects.filter(catagory='LS')
 return render(request,'app/topwear.html',{'topwears':topwears})



# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
from .forms import CustomerRegForm
class customerregistrationView(View):
    def get(self, request):
        form = CustomerRegForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login')  # Redirect to a success URL after form submission
    # Handling the case where form is not valid but has no errors
        elif form.errors:
            return render(request, 'app/customerregistration.html', {'form': form})
        else:
        # Handle the case where form is not valid but has no errors
        # You might want to log this or handle it differently
        # For now, let's render the form with the existing data
            return render(request, 'app/customerregistration.html', {'form': form})

class ProfileView(View):
    
    def get(self, request):
        # Retrieve the customer object associated with the current user
        #customer= Customer.objects.get(user=request.user)

        # Initialize the form with instance if exists
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form})

    
    def post(self, request):
        form = CustomerProfileForm(request.POST)  # Bind data to the form
        if form.is_valid():  
            # Save the form with the current user
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            # Redirect to a success page or any other URL
            return redirect('/address')
        else:
            # If form data is not valid, re-render the form with errors
            return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


    


def checkout(request):
 user=request.user
 address=Customer.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 70
 tot_amount = 0.0
 cartitems = Cart.objects.filter(user=user)
 if cartitems:
    for p in cartitems:
        temp_amount = (p.quantity * p.product.discount_price)
        amount += temp_amount
    tot_amount = amount + shipping_amount           
 context={'address':address,'cartitems':cartitems,'tot_amount':tot_amount}

 return render(request, 'app/checkout.html',context)

def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")
 


class EditAddressView(View):
    def get(self, request, pk):
        try:
            address = Customer.objects.get(id=pk)
            form = CustomerProfileForm(instance=address)
            return render(request, 'app/edit_address.html', {'form': form})
        except Customer.DoesNotExist:
            return redirect('address')
        
    def post(self, request, pk):  # Need to accept the primary key as well
        try:
            address = Customer.objects.get(id=pk)
            form = CustomerProfileForm(request.POST, instance=address)
            if form.is_valid():
                form.save()
                return redirect('address')  # Redirect to address page after successful edit
            else:
                # If form is not valid, re-render the edit form with errors
                return render(request, 'app/edit_address.html', {'form': form})
        except Customer.DoesNotExist:
            return redirect('address')

def deleteAddressView(request, pk):
    # Retrieve the address instance
    address = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        # If the request method is POST, it means the user confirmed the deletion
        address.delete()
        # Redirect to the address page or any other appropriate page
        return redirect('address')

    # If the request method is not POST, render a confirmation template
    return render(request, 'app/delete_address.html', {'address': address})


def Removeitem_cart(request,id):
   user=request.user
   item=Cart.objects.get(id=id)
   item.delete()
   return redirect('/showcart')


from django.core.exceptions import ObjectDoesNotExist

def Plus_cart(request):
    if request.method == "GET":
        try:
            prod_id = request.GET["prod_id"]
            user = request.user
            c = Cart.objects.get(product=prod_id, user=user)
            c.quantity += 1
            c.save()
            amount = 0.0
            shipping_amount = 70
            tot_amount = 0.0
            cart_product = Cart.objects.filter(user=user)
            if cart_product:
                for p in cart_product:
                    temp_amount = (p.quantity * p.product.discount_price)
                    amount += temp_amount
                tot_amount = amount + shipping_amount
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': tot_amount
            }
            return JsonResponse(data)
        except ObjectDoesNotExist:
            # Handle the case where the Cart object does not exist
            return JsonResponse({'error': 'Cart matching query does not exist'}, status=404)
def Minus_cart(request):
    if request.method == "GET":
        try:
            prod_id = request.GET["prod_id"]
            user = request.user
            c = Cart.objects.get(product=prod_id, user=user)
            c.quantity -= 1
            c.save()
            amount = 0.0
            shipping_amount = 70
            tot_amount = 0.0
            cart_product = Cart.objects.filter(user=user)
            if cart_product:
                for p in cart_product:
                    temp_amount = (p.quantity * p.product.discount_price)
                    amount += temp_amount
                tot_amount = amount + shipping_amount
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': tot_amount
            }
            return JsonResponse(data)
        except ObjectDoesNotExist:
            # Handle the case where the Cart object does not exist
            return JsonResponse({'error': 'Cart matching query does not exist'}, status=404)


