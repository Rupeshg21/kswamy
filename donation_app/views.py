from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Donor, Expense, RenovationGoal
from .serializers import (
    DonorSerializer, 
    ExpenseSerializer, 
    RenovationGoalSerializer,
    DashboardStatsSerializer
)

class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    
    def get_queryset(self):
        queryset = Donor.objects.all()
        search = self.request.query_params.get('search', None)
        payment_method = self.request.query_params.get('payment_method', None)
        
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) |
                models.Q(email__icontains=search) |
                models.Q(phone__icontains=search)
            )
        
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        stats = {
            'total_donations': Donor.objects.aggregate(total=Sum('amount'))['total'] or 0,
            'count': Donor.objects.count(),
            'by_payment_method': Donor.objects.values('payment_method')
                .annotate(total=Sum('amount'), count=Count('id'))
                .order_by('-total')
        }
        return Response(stats)

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    
    def get_queryset(self):
        queryset = Expense.objects.all()
        search = self.request.query_params.get('search', None)
        category = self.request.query_params.get('category', None)
        
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(notes__icontains=search)
            )
        
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        stats = {
            'total_expenses': Expense.objects.aggregate(total=Sum('amount'))['total'] or 0,
            'count': Expense.objects.count(),
            'by_category': Expense.objects.values('category')
                .annotate(total=Sum('amount'), count=Count('id'))
                .order_by('-total')
        }
        return Response(stats)

class RenovationGoalViewSet(viewsets.ModelViewSet):
    queryset = RenovationGoal.objects.filter(is_active=True)
    serializer_class = RenovationGoalSerializer

class DashboardView(APIView):
    def get(self, request):
        total_donations = Donor.objects.aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
        available_balance = total_donations - total_expenses
        donation_count = Donor.objects.count()
        expense_count = Expense.objects.count()
        
        # Get active renovation goal
        try:
            renovation_goal = RenovationGoal.objects.get(is_active=True)
            goal_amount = renovation_goal.goal_amount
        except RenovationGoal.DoesNotExist:
            goal_amount = 5000000  # Default goal
        
        progress_percentage = (total_donations / goal_amount * 100) if goal_amount > 0 else 0
        
        data = {
            'total_donations': total_donations,
            'total_expenses': total_expenses,
            'available_balance': available_balance,
            'donation_count': donation_count,
            'expense_count': expense_count,
            'renovation_goal': goal_amount,
            'progress_percentage': progress_percentage
        }
        
        serializer = DashboardStatsSerializer(data)
        return Response(serializer.data)

class RecentActivityView(APIView):
    def get(self, request):
        recent_donations = Donor.objects.all().order_by('-date', '-created_at')[:5]
        recent_expenses = Expense.objects.all().order_by('-date', '-created_at')[:5]
        
        data = {
            'recent_donations': DonorSerializer(recent_donations, many=True).data,
            'recent_expenses': ExpenseSerializer(recent_expenses, many=True).data
        }
        return Response(data)

class ChartsDataView(APIView):
    def get(self, request):
        # Donations by payment method
        donations_by_payment = Donor.objects.values('payment_method') \
            .annotate(total=Sum('amount')) \
            .order_by('-total')
        
        # Expenses by category
        expenses_by_category = Expense.objects.values('category') \
            .annotate(total=Sum('amount')) \
            .order_by('-total')
        
        # Monthly trends
        monthly_donations = Donor.objects.annotate(month=TruncMonth('date')) \
            .values('month') \
            .annotate(total=Sum('amount')) \
            .order_by('month')[:12]
        
        monthly_expenses = Expense.objects.annotate(month=TruncMonth('date')) \
            .values('month') \
            .annotate(total=Sum('amount')) \
            .order_by('month')[:12]
        
        data = {
            'donations_by_payment': list(donations_by_payment),
            'expenses_by_category': list(expenses_by_category),
            'monthly_donations': list(monthly_donations),
            'monthly_expenses': list(monthly_expenses)
        }
        
        return Response(data)