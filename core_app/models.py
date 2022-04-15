from secrets import choice
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (                                           # User Roles
        (1, 'Tax Payer'),
        (2, 'Tax Accountant'),
        (3, 'SuperUser')
    )
    
    TAX_CHOICES = (
        (1, 'New'),
        (2, 'Paid'),
        (3, 'Delayed')
    )
    
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    name = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    income_from_salary = models.IntegerField(null=True, blank=True)
    income_from_shares = models.IntegerField(null=True, blank=True)
    tax_status = models.PositiveSmallIntegerField(choices=TAX_CHOICES, null=True, blank=True)
    
    USERNAME_FIELD  = 'username'                                    
    REQUIRED_FIELDS = ['password']
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name_plural = "User"
        db_table = "User"