from django.db import models

# Create your models here.


class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(Timestamp):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(Timestamp):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door')
    )

    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.TextField(null=True)


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out of delivery', 'Out of delivery'),
        ('Delivered', 'Delivered')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)