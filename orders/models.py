from django.db import models
from django.contrib.auth.models import User

class OfficerProfile(models.Model):
    RANK_CHOICES = [
        ('2LT', 'Second Lieutenant'),
        ('LT', 'Lieutenant'),
        ('CAPT', 'Captain'),
        ('MAJ', 'Major'),
        ('LT_COL', 'Lieutenant Colonel'),
        ('COL', 'Colonel'),
        ('BRIG', 'Brigadier'),
        ('MAJ_GEN', 'Major General'),
        ('LT_GEN', 'Lieutenant General'),
        ('GEN', 'General'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service_number = models.CharField(max_length=30, unique=True)
    rank = models.CharField(max_length=10, choices=RANK_CHOICES)
    office_location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.get_rank_display()} {self.user.first_name} {self.user.last_name} ({self.service_number})"


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('BREAKFAST', 'Breakfast Profile'),
        ('LUNCH', 'Lunch Profile'),
        ('DINNER', 'Supper/Dinner Profile'),
        ('DRINK', 'Soft Drinks Profile'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    # Added price field (Defaulting to KES 0.00, allows up to 9999.99)
    price = models.DecimalField(max_length=10, max_digits=6, decimal_places=2, default=0.00)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - KSh {self.price}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('ACCEPTED', 'Accepted by Mess Admin'),
        ('CANCELLED', 'Cancelled by Officer'),
    ]
    
    officer = models.ForeignKey(OfficerProfile, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} via {self.officer.user.last_name}"