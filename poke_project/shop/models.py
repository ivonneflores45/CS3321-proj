from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

'''
Models
Author(s): Maryam Khan
Date created: 4/2/2026
'''

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class Listing(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('removed', 'Removed'),
    ]
    CATEGORY_CHOICES = [
        ('single_card', 'Single Card'),
        ('booster_pack', 'Booster Pack'),
        ('booster_box', 'Booster Box'),
    ]
    TYPE_CHOICES = [
        ('pokemon', 'Pokemon'),
        ('trainer', 'Trainer'),
        ('energy', 'Energy'),
    ]
    CONDITION_CHOICES = [
        ('mint', 'Mint'),
        ('near_mint', 'Near Mint'),
        ('used', 'Used'),
        ('damaged', 'Damaged'),
    ]
    RARITY_CHOICES = [
        ('common', 'Common'),
        ('uncommon', 'Uncommon'),
        ('rare', 'Rare'),
        ('promo', 'Promo'),
    ]
    TYPE_CHOICES = [
        ('pokemon', 'Pokemon'),
        ('trainer', 'Trainer'),
        ('energy', 'Energy')
    ]
    ABILITY_CHOICES = [
        ('ability', 'Ability'),
        ('attack', 'Attack'),
        ('none', 'None'),
    ]
    ELEMENT_CHOICES = [
        ('fire', 'Fire'),
        ('water', 'Water'),
        ('grass', 'Grass'),
        ('electric', 'Electric'),
        ('psychic', 'Psychic'),
        ('fighting', 'Fighting'),
        ('dark', 'Dark'),
        ('metal', 'Metal'),
        ('fairy', 'Fairy'),
        ('dragon', 'Dragon'),
        ('colorless', 'Colorless'),
        ('none', 'None'),
    ]

    #attribute fields
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='files/images', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    set_name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    rarity = models.CharField(max_length=50, choices=RARITY_CHOICES)
    ability = models.CharField(max_length=50, choices=ABILITY_CHOICES)
    element = models.CharField(max_length=50, choices=ELEMENT_CHOICES)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    listing_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def is_available(self):
        return self.listing_status == 'active' and self.stock_quantity > 0
    
    def __str__(self):
        return self.title
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order{self.id} by {self.customer}"
    
class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_subtotal(self):
        return self.quantity * self.unit_price
    
    def __str__(self):
        return f"{self.quantity}x {self.listing.title}" #ex: 2x Energy Card

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    ] 

    PAYMENT_CHOICES = [
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    payment_date = models.DateTimeField(default=timezone.now)
    transaction_id = models.CharField(max_length=200, blank=True)

    def is_sucessful(self):
        return self.payment_status == 'completed'
    
    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id}"
    
class ShippingInfo(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=200)
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200, blank=True)
    city =  models.CharField(max_length=100)
    state =  models.CharField(max_length=100)
    zip_code =  models.CharField(max_length=10)
    country = models.CharField(max_length=200)
    tracking_number = models.CharField(max_length=200, blank=True)
    shipping_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')

    def get_full_address(self):
       parts = [self.address_line1]
       if self.address_line2:
           parts.append(self.address_line2)
       parts.append(f"{self.city}, {self.state}, {self.zip_code}, {self.country}")
       return ', '.join(parts)
    
    def __str__(self):
        return f"Shipping for Order {self.order.id} to {self.recipient_name}"
    

        