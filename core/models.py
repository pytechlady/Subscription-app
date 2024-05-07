from django.db import models

# Create your models here.
class Company(models.Model):
    company_name = models.CharField(max_length=150)
    company_identifier = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.company_name} - {self.company_identifier}"
    
    
class Subscription(models.Model):
    subscription_name = models.CharField(max_length=50)
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='subscription')
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.subscription_name} - {self.company_name.company_identifier} - {self.company_name.company_name}"
    
    
class UserSubscription(models.Model):
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='user')
    user_identifier = models.CharField(max_length=250)
    subscription_name = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="user_sub")
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.company_name.company_name} - {self.company_name.company_identifier} - {self.user_identifier}"