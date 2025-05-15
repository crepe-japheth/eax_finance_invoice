import calendar
from django.utils import timezone
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
import json
from datetime import datetime, timedelta, date
from invoice.models import Invoice

def invoice_line_dashboard():
    # Get data for the last 30 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Group invoices by created_at date and sum amounts
    invoices_by_date = Invoice.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        total_amount=Sum('amount')
    ).order_by('date')
    
    # Prepare data for the chart
    dates = []
    amounts = []
    
    for item in invoices_by_date:
        dates.append(item['date'].strftime('%Y-%m-%d'))
        amounts.append(float(item['total_amount']))
    
    # Pass data to the template
    data = {
        'chart_dates': dates,
        'chart_amounts': amounts
    }
    
    return data


def get_week_range(date_obj):
    """
    Returns the start and end dates for the week containing the given date.
    Weeks are considered to start on Monday and end on Sunday.
    """
    # Get the day of the week (0 is Monday, 6 is Sunday in Python's datetime)
    day_of_week = date_obj.weekday()
    
    # Calculate start of week (Monday)
    start_of_week = date_obj - timedelta(days=day_of_week)
    
    # Calculate end of week (Sunday)
    end_of_week = start_of_week + timedelta(days=6)
    
    return start_of_week, end_of_week



def get_current_month_weeks():
    """
    Returns a list of tuples containing (week_start_date, week_end_date, week_label)
    for each week in the current month.
    """
    today = date.today()
    current_month = today.month
    current_year = today.year
    
    # Get first day of the month
    first_day = date(current_year, current_month, 1)
    
    # Get last day of the month
    last_day = date(current_year, current_month, 
                    calendar.monthrange(current_year, current_month)[1])
    
    # Get the week containing the first day of the month
    first_week_start, first_week_end = get_week_range(first_day)
    
    # Make sure we don't go beyond the month
    if first_week_end > last_day:
        first_week_end = last_day
    
    weeks = []
    week_count = 1
    
    # Add the first week
    weeks.append((
        first_week_start,
        first_week_end,
        f"Week {week_count}"
    ))
    
    # Start with the day after the first week ends
    current_date = first_week_end + timedelta(days=1)
    
    # Continue until we reach the end of the month
    while current_date <= last_day:
        week_count += 1
        week_start, week_end = get_week_range(current_date)
        
        # Make sure we don't go beyond the month
        if week_end > last_day:
            week_end = last_day
        
        weeks.append((
            week_start,
            week_end,
            f"Week {week_count}"
        ))
        
        # Move to the next week
        current_date = week_end + timedelta(days=1)
    
    return weeks



def weekly_invoice_status_chart():
    """
    Returns data for a bar chart showing weekly totals of paid and pending/incomplete invoices
    for the current month.
    """
    # Get the weeks in the current month
    weeks = get_current_month_weeks()
    
    # Initialize data structures for the chart
    week_labels = []
    paid_amounts = []
    pending_incomplete_amounts = []
    
    # Process each week
    for week_start, week_end, week_label in weeks:
        # Add the week label
        week_labels.append(week_label)
        
        # Query for invoices in this date range
        week_invoices = Invoice.objects.filter(
            date_received__gte=week_start,
            date_received__lte=week_end
        )
        
        # Sum the paid invoices
        paid_total = week_invoices.filter(
            status='Paid'
        ).aggregate(
            total=Sum('amount', default=0)
        )['total'] or 0
        
        # Sum the pending/incomplete invoices
        pending_incomplete_total = week_invoices.filter(
            status__in=['Pending', 'Incomplete']
        ).aggregate(
            total=Sum('amount', default=0)
        )['total'] or 0
        
        # Add the totals to our lists
        paid_amounts.append(float(paid_total))
        pending_incomplete_amounts.append(float(pending_incomplete_total))
    
    # Prepare the context for the template
    context = {
        'week_labels': week_labels,
        'paid_amounts': paid_amounts,
        'pending_incomplete_amounts': pending_incomplete_amounts,
        'current_month': datetime.now().strftime('%B %Y')
    }
    
    return context


def get_yearly_status_totals(year=None):
    """
    Retrieves total amounts for each invoice status (Pending, Paid, Incomplete) for the specified year.
    If no year is provided, it defaults to the current year.
    
    Returns a dictionary with status totals and counts.
    """
    # Default to current year if not specified
    if year is None:
        year = timezone.now().year
    
    # Define date range for the year
    # After (fixed code)
    start_date = timezone.make_aware(datetime(year, 1, 1))
    end_date = timezone.make_aware(datetime(year, 12, 31, 23, 59, 59))
    
    # Query invoices for the specified year
    yearly_invoices = Invoice.objects.filter(
        created_at__gte=start_date,
        created_at__lte=end_date
    )
    
    # Get total amount for each status
    paid_total = yearly_invoices.filter(status='Paid').aggregate(
        total=Sum('amount', default=0),
        count=Count('id')
    )
    
    pending_total = yearly_invoices.filter(status='Pending').aggregate(
        total=Sum('amount', default=0),
        count=Count('id')
    )
    
    incomplete_total = yearly_invoices.filter(status='Incomplete').aggregate(
        total=Sum('amount', default=0),
        count=Count('id')
    )
    
    # Calculate grand total
    grand_total = yearly_invoices.aggregate(
        total=Sum('amount', default=0),
        count=Count('id')
    )
    
    # Format results as a dictionary
    results = {
        'year': year,
        'paid': {
            'amount': float(paid_total['total'] or 0),
            'count': paid_total['count'],
            'percentage': calculate_percentage(paid_total['total'], grand_total['total'])
        },
        'pending': {
            'amount': float(pending_total['total'] or 0),
            'count': pending_total['count'],
            'percentage': calculate_percentage(pending_total['total'], grand_total['total'])
        },
        'incomplete': {
            'amount': float(incomplete_total['total'] or 0),
            'count': incomplete_total['count'],
            'percentage': calculate_percentage(incomplete_total['total'], grand_total['total'])
        },
        'total': {
            'amount': float(grand_total['total'] or 0),
            'count': grand_total['count']
        }
    }
    
    return results

def calculate_percentage(amount, total):
    """Calculate percentage with handling for zero division"""
    if total is None or total == 0:
        return 0
    if amount is None:
        return 0
    return round((float(amount) / float(total)) * 100, 2)
