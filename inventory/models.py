from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name
class Feed(models.Model):
    CATEGORY_CHOICES = [
        ('Poultry', 'Poultry'),
        ('Cattle', 'Cattle'),
        ('Goat', 'Goat'),
        ('Pet', 'Pet'),
        ('Others', 'Others'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

    purchase_price = models.DecimalField(max_digits=8, decimal_places=2)
    selling_price = models.DecimalField(max_digits=8, decimal_places=2)

    expiry_date = models.DateField()

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        default=1
    )

    def __str__(self):
        return self.name


class Purchase(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        default=1   # SKM
    )

    quantity = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=8, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.feed.name} - {self.quantity}"



class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.name
class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=8, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.feed.name}"

    
class Payment(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
