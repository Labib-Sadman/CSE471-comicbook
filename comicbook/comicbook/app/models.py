# models.py

from django.db import models
from django.contrib.auth.models import User

STATE_CHOICES = (
    ('Dhaka Division', 'Dhaka Division'),
    ('Chattogram Division', 'Chattogram Division'),
    ('Khulna Division', 'Khulna Division'),
    ('Barishal Division', 'Barishal Division'),
    ('Sylhet Division', 'Sylhet Division'),
    ('Rangpur Division', 'Rangpur Division'),
    ('Mymensingh Division', 'Mymensingh Division')
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)


CATEGORY_CHOICES = (
    ("S", "Superhero"),
    ("NF", "Non-fiction"),
    ("SF", "Science-Fiction"),
    ("H", "Horror"),
)


class Productdata(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to="productimg")
    images = models.ManyToManyField('ProductImage', blank=True)

    def __str__(self):
        return str(self.id)


class ProductImage(models.Model):
    product = models.ForeignKey(Productdata, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return f"{self.product.title} - Image {self.id}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Productdata, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price

STATUS_CHOICES = (
    ("Accepted", "Accepted"),
    ("Packed", "Packed"),
    ("On The Way", "On The Way"),
    ("Cancel", "Cancel"),
    ("Delivered", "Delivered"),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Productdata, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price
