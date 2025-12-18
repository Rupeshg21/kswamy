from django.db import models

class Donor(models.Model):
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cheque', 'Cheque'),
    ]
    
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.name} - ₹{self.amount}"

class Expense(models.Model):
    CATEGORIES = [
        ('Construction', 'Construction'),
        ('Materials', 'Materials'),
        ('Labor', 'Labor'),
        ('Decoration', 'Decoration'),
        ('Electrical', 'Electrical'),
        ('Plumbing', 'Plumbing'),
        ('Other', 'Other'),
    ]
    
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.title} - ₹{self.amount}"

class RenovationGoal(models.Model):
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2, default=5000000)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    target_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Renovation Goal: ₹{self.goal_amount}"