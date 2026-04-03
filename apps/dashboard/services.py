from django.db.models import Sum
from django.db.models.functions import TruncMonth
from apps.records.models import FinancialRecord

def get_user_totals(user):
    """Return total income, total expense, and balance for the user"""
    totals = FinancialRecord.objects.filter(user=user).values('type').annotate(total_amount=Sum('amount'))

    total_income = sum(item['total_amount'] for item in totals if item['type'] == 'income')
    total_expense = sum(item['total_amount'] for item in totals if item['type'] == 'expense')
    balance = total_income - total_expense

    return {
        "total_income": total_income or 0,
        "total_expense": total_expense or 0,
        "balance": balance or 0
    }

def get_category_totals(user, record_type=None):
    """Return totals grouped by category. Optional: filter by 'income' or 'expense'"""
    qs = FinancialRecord.objects.filter(user=user)
    if record_type in ['income', 'expense']:
        qs = qs.filter(type=record_type)

    return list(qs.values('category').annotate(total_amount=Sum('amount')).order_by('-total_amount'))

def get_monthly_analytics(user):
    """Return monthly totals for income and expense in the format: {YYYY-MM: {income: x, expense: y}}"""
    qs = FinancialRecord.objects.filter(user=user)
    monthly = qs.annotate(month=TruncMonth('date')).values('month', 'type').annotate(total_amount=Sum('amount')).order_by('month')

    result = {}
    for item in monthly:
        month_str = item['month'].strftime('%Y-%m')
        if month_str not in result:
            result[month_str] = {"income": 0, "expense": 0}
        result[month_str][item['type']] = item['total_amount']

    return result