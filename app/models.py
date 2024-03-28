from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.
state_choices=(
  ('Andaman and Nicobar Island','Andaman and Nicobar Island'),
('Ap','Ap'),
('Assam','Assam'),
('Bihar','Bihar'),
('Chandigarh','Chandigarh'),
('Chatishgarh','Chatishgarh')
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    locality = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    zipcode = models.IntegerField(null=True, blank=True)  # Allow null values for optional field
    state = models.CharField(choices=state_choices, max_length=120)

    def __str__(self):
        return str(self.id)
  
catagory_choices=(
  ('M','mobile'),
  ('L','Laptop'),
  ('BW','Bottom wear'),
  ('TW','Top wear'),
  ('LS','Ladies'),
  ('LB','Ladies Bottomwear')
)  

class Product(models.Model):
  title=models.CharField(max_length=120)
  selling_price=models.FloatField()
  discount_price=models.FloatField()
  describtion=models.TextField()
  brand=models.CharField(max_length=120)
  catagory=models.CharField(choices=catagory_choices,max_length=3)
  product_img=models.ImageField(upload_to='productimg')
  def __str__(self) :
    return str(self.id)
  
class Cart(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  product=models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity=models.PositiveIntegerField(default=1)
  def __str__(self) :
    return str(self.id)
  @property
  def total_cost(self):
     return self.quantity*self.product.discount_price
  
status_choices=(
  ('Accepted','Accepted'),
  ('packed','packed'),
  ('on the way','on the way'),
  ('delivered','delivered'),
  ('cancel','cancel')
)  

class OrderPlaced(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  quantity=models.PositiveIntegerField(default=1)
  order_date=models.DateTimeField(auto_now_add=True)
  status=models.CharField(choices=status_choices,max_length=120,default='pending')
  
    
  