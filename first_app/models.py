from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class Registration(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=128, default=make_password('default_password'))  # Store hashed password with default
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"Username: {self.username} | Email: {self.email} | Name: {self.name} | Phone: {self.phone} | Password: {self.password} | Created: {self.created_at.strftime('%Y-%m-%d %H:%M')} | Updated: {self.updated_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Registration"
        verbose_name_plural = "Registrations"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.email} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ['-created_at']

class Franchise(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('IN_PROGRESS', 'In Progress'),
            ('CONTACTED', 'Contacted'),
            ('REJECTED', 'Rejected'),
            ('APPROVED', 'Approved')
        ],
        default='PENDING'
    )

    def __str__(self):
        return f"{self.name} - {self.email} - {self.status} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Franchise"
        verbose_name_plural = "Franchises"
        ordering = ['-created_at']

class TradingConfiguration(models.Model):
    CATEGORY_CHOICES = [
        ('FOREX', 'Forex'),
        ('COMEX', 'Comex'),
        ('STOCKS', 'Stocks'),
        ('CRYPTO', 'Crypto'),
    ]

    user = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='trading_configs')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    symbol = models.CharField(max_length=20)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'category', 'symbol']
        ordering = ['category', 'symbol']

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.symbol}"
