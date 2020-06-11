from django.db import models

from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.utils.timezone import now
import datetime


class Venues(models.Model):
    Venue_Name = models.CharField(max_length=50, null=False, blank=False)
    Maximum_Guest = models.IntegerField(null=False, blank=False)
    Price_per_Day = models.IntegerField(null=False, blank=False)
    Address = models.CharField(max_length=255, null=False, blank=False)
    City = models.CharField(max_length=50, null=False, blank=False)
    Phone = models.CharField(
        blank=False, help_text='Contact phone number', default=0, max_length=15)
    image1 = models.ImageField(
        upload_to='picture/', max_length=255, null=True, blank=True)
    image2 = models.ImageField(
        upload_to='picture/', max_length=255, null=True, blank=True)
    image3 = models.ImageField(
        upload_to='picture/', max_length=255, null=True, blank=True)
    image4 = models.ImageField(
        upload_to='picture/', max_length=255, null=True, blank=True)
    image5 = models.ImageField(
        upload_to='picture/', max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.Venue_Name)


class Trucks(models.Model):
    Model_Name = models.CharField(max_length=50, null=False, blank=False)
    Price = models.IntegerField(null=False, blank=False)
    Description = models.CharField(max_length=255, null=False, blank=False)
    image1 = models.ImageField(
        upload_to='picture/', max_length=255, null=True, blank=True)
    image2 = models.ImageField(
        upload_to='picture/', max_length=255, null=True, blank=True)
    image3 = models.ImageField(
        upload_to='picture/', max_length=255, null=True, blank=True)
    image4 = models.ImageField(
        upload_to='picture/', max_length=255, null=True, blank=True)
    image5 = models.ImageField(
        upload_to='picture/', max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.Model_Name)

        
class Special(models.Model):
    SPECIALITY_CHOICES = (
        ('North Indian', 'North Indian'),
        ('South Indian', 'South Indian'),
        ('Gujarati', 'Gujarati'),
        ('Bengali', 'Bengali'),
        ('Bakery', 'Bakery'),
        ('Marathi', 'Marathi'),
        ('Continental', 'Continental'),
        ('Jain Food', 'Jain Food'),
        ('Rajasthani', 'Rajasthani'),
        ('Punjabi', 'Punjabi'),
    
    )
    speciality = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.speciality)

class Chef(models.Model):
    Work_As = ArrayField(ArrayField(models.CharField(
        max_length=200, null=False, blank=False)))
    Name = models.CharField(max_length=50, null=False, blank=False)
    Phone = models.CharField(max_length=15, null=False, blank=False)
    Email = models.EmailField(max_length=50, null=True, blank=True)
    Stipend = models.IntegerField(null=True, blank=True)
    Country = models.CharField(
        null=False, max_length=50, blank=False, default="India")
    State = models.CharField(max_length=100, null=False, blank=False)
    City = models.CharField(max_length=100, null=False, blank=False)
    Area = models.CharField(max_length=250, null=False, blank=False)
    Address = models.CharField(max_length=255, null=False, blank=False)
    # Speciality = ArrayField(ArrayField(models.CharField(
    #     max_length=250, null=False, blank=False)))
    Speciality = models.ManyToManyField(Special)

    Type = models.CharField(max_length=15, null=False, blank=False)
    ExpertIn = models.CharField(max_length=100, null=False, blank=False)
    License = models.CharField(max_length=5, null=False, blank=False)
    Base = models.CharField(max_length=100, null=True, blank=True)
    EmployeeID = models.CharField(max_length=100, null=True, blank=True)
    Image = models.ImageField(upload_to='picture/',
                              max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.Name)


class Ordered_Venue(models.Model):
    venue_id = models.IntegerField(null=False, blank=False)
    start = models.DateField(null=False, blank=False)
    end = models.DateField(null=False, blank=False)


class Ordered_Chef(models.Model):
    chef_id = models.IntegerField(null=False, blank=False)
    start = models.DateField(null=False, blank=False)
    end = models.DateField(null=False, blank=False)


class Customer(models.Model):
    user = models.OneToOneField(User , on_delete= models.CASCADE, null= True , blank= True)
    name= models.CharField(max_length=200, null= True)
    email=  models.CharField(max_length=200, null= True)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    name= models.CharField(max_length=200, null= True)
    price=  models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)


    def __str__(self):
        return str(self.name)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank= True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete= models.BooleanField(default=False, null=True, blank=False)
    transaction_id= models.CharField(max_length=200, null= True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitemstruck = self.orderitemtruck_set.all()
        total1 = sum([item.get_total for item in orderitemstruck])
        
        orderitemsvenue = self.orderitemvenue_set.all()
        total2 = sum([item.get_total for item in orderitemsvenue])

        orderitemschef = self.orderitemchef_set.all()
        total3 = sum([item.get_total for item in orderitemschef])

        return total1+total2+total3


class OrderItemTruck(models.Model):
    truck= models.ForeignKey(Trucks, on_delete=models.SET_NULL, blank= True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank= True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)


    @property
    def get_total(self):
        total = self.truck.Price * self.quantity
        return total

class OrderItemVenue(models.Model):
    venue = models.ForeignKey(Venues, on_delete=models.SET_NULL, blank= True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank= True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    start = models.DateField(null=False, blank=False, default = now)
    end = models.DateField(null=False, blank=False, default = now)

    @property
    def get_total(self):
        format = "%Y-%m-%d"
        start = datetime.datetime.strptime(str(self.start), format)
        end = datetime.datetime.strptime(str(self.end), format)
        start = start.date()
        end = end.date()
        days = (end-start).days
        total = self.venue.Price_per_Day * self.quantity * days
        return total

class OrderItemChef(models.Model):
    chef = models.ForeignKey(Chef, on_delete=models.SET_NULL, blank= True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank= True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    start = models.DateField(null=False, blank=False, default = now)
    end = models.DateField(null=False, blank=False, default = now)
    @property
    def get_total(self):
        format = "%Y-%m-%d"
        start = datetime.datetime.strptime(str(self.start), format)
        end = datetime.datetime.strptime(str(self.end), format)
        start = start.date()
        end = end.date()
        days = (end-start).days
        total = self.chef.Stipend * self.quantity * days
        return total

class ReviewIndex(models.Model):
    Name = models.CharField(null = False , blank = False , max_length = 200)
    Review = models.CharField(null = False , blank = False , max_length = 1024)

class ReviewTruck(models.Model):
    Name = models.CharField(null = False , blank = False , max_length = 200)
    Review = models.CharField(null = False , blank = False , max_length = 1024)

class ReviewChef(models.Model):
    Name = models.CharField(null = False , blank = False , max_length = 200)
    Review = models.CharField(null = False , blank = False , max_length = 1024)

class ReviewVenue(models.Model):
    Name = models.CharField(null = False , blank = False , max_length = 200)
    Review = models.CharField(null = False , blank = False , max_length = 1024)

class ReviewOutlet(models.Model):
    Name = models.CharField(null = False , blank = False , max_length = 200)
    Review = models.CharField(null = False , blank = False , max_length = 1024)

class ReviewVenueID(models.Model):
    venue_id = models.IntegerField(null = False , blank = False)
    Name = models.CharField(null = False , blank = False , max_length = 200)
    Review = models.CharField(null = False , blank = False , max_length = 1024)

class ReviewChefID(models.Model):
    chef_id = models.IntegerField(null = False , blank = False)
    Name = models.CharField(null = False , blank = False , max_length = 200)
    Review = models.CharField(null = False , blank = False , max_length = 1024)

class ReviewTruckID(models.Model):
    truck_id = models.IntegerField(null = False , blank = False)
    Name = models.CharField(null = False , blank = False , max_length = 200)
    Review = models.CharField(null = False , blank = False , max_length = 1024)

class Transactions(models.Model):
    CustomerID = models.IntegerField()
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=255, null=True, blank=True)
    checksum = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
