from django.contrib import admin
from .models import Donor, Expense, RenovationGoal

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'payment_method', 'date')
    list_filter = ('payment_method', 'date')
    search_fields = ('name', 'email', 'phone')
    ordering = ('-date',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'amount', 'date')
    list_filter = ('category', 'date')
    search_fields = ('title', 'notes')
    ordering = ('-date',)

@admin.register(RenovationGoal)
class RenovationGoalAdmin(admin.ModelAdmin):
    list_display = ('goal_amount', 'start_date', 'target_date', 'is_active')
    list_filter = ('is_active',)