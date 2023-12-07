from django.db import models


class Item(models.Model):

    """Model representing a product item."""

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class Discount(models.Model):

    """Model representing a discount."""

    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    

class Tax(models.Model):

    """Model representing a tax."""

    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    

class Order(models.Model):

    """Model representing an order."""


    items = models.ManyToManyField(Item)
    taxes = models.ManyToManyField(Tax)
    discounts = models.ManyToManyField(Discount)

    @property
    def items_price(self):
        """Calculate the total price of items in the order."""

        item_price = sum([item.price for item in self.items.all()])

        return item_price
    
    @property
    def total_price(self):
        """Calculate the total price of the order with discounts and taxes."""
        
        discount_amount = sum([discount.amount for discount in self.discounts.all()])
        tax_amount = sum([tax.amount for tax in self.taxes.all()])
        return self.items_price - discount_amount + tax_amount
    
    def __str__(self):
        return f"Order #{self.pk}"


    

