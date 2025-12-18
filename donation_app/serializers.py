from rest_framework import serializers
from .models import Donor, Expense, RenovationGoal

class DonorSerializer(serializers.ModelSerializer):
    formatted_amount = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()
    
    class Meta:
        model = Donor
        fields = '__all__'
    
    def get_formatted_amount(self, obj):
        return f"₹{obj.amount:,.0f}"
    
    def get_formatted_date(self, obj):
        return obj.date.strftime("%d %b %Y")

class ExpenseSerializer(serializers.ModelSerializer):
    formatted_amount = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()
    
    class Meta:
        model = Expense
        fields = '__all__'
    
    def get_formatted_amount(self, obj):
        return f"₹{obj.amount:,.0f}"
    
    def get_formatted_date(self, obj):
        return obj.date.strftime("%d %b %Y")

class RenovationGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = RenovationGoal
        fields = '__all__'

class DashboardStatsSerializer(serializers.Serializer):
    total_donations = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    available_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    donation_count = serializers.IntegerField()
    expense_count = serializers.IntegerField()
    renovation_goal = serializers.DecimalField(max_digits=12, decimal_places=2)
    progress_percentage = serializers.FloatField()