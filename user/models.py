from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(TimeStampMixin, AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    lat = models.DecimalField(decimal_places = 10, max_digits = 15, null=False, blank = False)
    long = models.DecimalField(decimal_places = 10, max_digits = 15, null=False, blank = False)
    infected_1 = models.PositiveIntegerField(null=True,  blank=True)
    infected_2 = models.PositiveIntegerField(null=True, blank=True)
    infected_3 = models.PositiveIntegerField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

    class Meta:
        db_table = "user"


class InventoryDetails(TimeStampMixin):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    points = models.PositiveIntegerField(null=False, blank=False)

    class Meta:
        db_table = "inventory_details"
        

class UserInventory(TimeStampMixin):
    user_id = models.PositiveIntegerField(null=False, blank=False)
    inventory_id = models.PositiveIntegerField(null=False, blank=False)
    qty = models.PositiveIntegerField(null=False, blank=False)

    class Meta:
        db_table = "user_inventory"