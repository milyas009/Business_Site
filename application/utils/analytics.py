from datetime import datetime, timedelta
from application.models import User, Franchise, Transaction, AnalyticsData
from mongoengine.queryset.visitor import Q

def calculate_growth_rate(model, time_range):
    """Calculate growth rate for a given model over a time range"""
    now = datetime.utcnow()
    
    if time_range == 'day':
        current_period = now - timedelta(days=1)
        previous_period = current_period - timedelta(days=1)
    elif time_range == 'week':
        current_period = now - timedelta(weeks=1)
        previous_period = current_period - timedelta(weeks=1)
    elif time_range == 'month':
        current_period = now - timedelta(days=30)
        previous_period = current_period - timedelta(days=30)
    else:  # year
        current_period = now - timedelta(days=365)
        previous_period = current_period - timedelta(days=365)
    
    current_count = model.objects(created_at__gte=current_period).count()
    previous_count = model.objects(
        Q(created_at__gte=previous_period) & Q(created_at__lt=current_period)
    ).count()
    
    if previous_count == 0:
        return 100.0 if current_count > 0 else 0.0
    
    return ((current_count - previous_count) / previous_count) * 100

def calculate_revenue_growth(time_range):
    """Calculate revenue growth over a time range"""
    now = datetime.utcnow()
    
    if time_range == 'day':
        current_period = now - timedelta(days=1)
        previous_period = current_period - timedelta(days=1)
    elif time_range == 'week':
        current_period = now - timedelta(weeks=1)
        previous_period = current_period - timedelta(weeks=1)
    elif time_range == 'month':
        current_period = now - timedelta(days=30)
        previous_period = current_period - timedelta(days=30)
    else:  # year
        current_period = now - timedelta(days=365)
        previous_period = current_period - timedelta(days=365)
    
    current_revenue = sum(t.amount for t in Transaction.objects(timestamp__gte=current_period))
    previous_revenue = sum(t.amount for t in Transaction.objects(
        Q(timestamp__gte=previous_period) & Q(timestamp__lt=current_period)
    ))
    
    if previous_revenue == 0:
        return 100.0 if current_revenue > 0 else 0.0
    
    return ((current_revenue - previous_revenue) / previous_revenue) * 100

def calculate_rating_growth(time_range):
    """Calculate average rating growth over a time range"""
    now = datetime.utcnow()
    
    if time_range == 'day':
        current_period = now - timedelta(days=1)
        previous_period = current_period - timedelta(days=1)
    elif time_range == 'week':
        current_period = now - timedelta(weeks=1)
        previous_period = current_period - timedelta(weeks=1)
    elif time_range == 'month':
        current_period = now - timedelta(days=30)
        previous_period = current_period - timedelta(days=30)
    else:  # year
        current_period = now - timedelta(days=365)
        previous_period = current_period - timedelta(days=365)
    
    current_rating = Franchise.objects(last_updated__gte=current_period).average('rating') or 0
    previous_rating = Franchise.objects(
        Q(last_updated__gte=previous_period) & Q(last_updated__lt=current_period)
    ).average('rating') or 0
    
    if previous_rating == 0:
        return 100.0 if current_rating > 0 else 0.0
    
    return ((current_rating - previous_rating) / previous_rating) * 100

def get_revenue_data(time_range):
    """Get revenue data for charting"""
    now = datetime.utcnow()
    
    if time_range == 'day':
        start_date = now - timedelta(days=1)
        interval = timedelta(hours=1)
        format_str = '%H:00'
    elif time_range == 'week':
        start_date = now - timedelta(weeks=1)
        interval = timedelta(days=1)
        format_str = '%a'
    elif time_range == 'month':
        start_date = now - timedelta(days=30)
        interval = timedelta(days=1)
        format_str = '%d'
    else:  # year
        start_date = now - timedelta(days=365)
        interval = timedelta(days=30)
        format_str = '%b'
    
    data = {'labels': [], 'values': []}
    current = start_date
    
    while current <= now:
        next_period = current + interval
        revenue = sum(t.amount for t in Transaction.objects(
            Q(timestamp__gte=current) & Q(timestamp__lt=next_period)
        ))
        
        data['labels'].append(current.strftime(format_str))
        data['values'].append(float(revenue))
        current = next_period
    
    return data

def get_user_demographics():
    """Get user demographic data"""
    total_users = User.objects.count()
    roles = User.objects.item_frequencies('role')
    
    return {
        'labels': list(roles.keys()),
        'values': [int((count / total_users) * 100) for count in roles.values()]
    }

def get_activity_data(time_range):
    """Get user activity data"""
    now = datetime.utcnow()
    
    if time_range == 'day':
        start_date = now - timedelta(days=1)
        interval = timedelta(hours=1)
        format_str = '%H:00'
    elif time_range == 'week':
        start_date = now - timedelta(weeks=1)
        interval = timedelta(days=1)
        format_str = '%a'
    elif time_range == 'month':
        start_date = now - timedelta(days=30)
        interval = timedelta(days=1)
        format_str = '%d'
    else:  # year
        start_date = now - timedelta(days=365)
        interval = timedelta(days=30)
        format_str = '%b'
    
    data = {'labels': [], 'values': []}
    current = start_date
    
    while current <= now:
        next_period = current + interval
        activity_count = AnalyticsData.objects(
            Q(timestamp__gte=current) & Q(timestamp__lt=next_period) &
            Q(metric='user_activity')
        ).count()
        
        data['labels'].append(current.strftime(format_str))
        data['values'].append(activity_count)
        current = next_period
    
    return data

def get_growth_data(time_range):
    """Get growth data for multiple metrics"""
    now = datetime.utcnow()
    
    if time_range == 'day':
        start_date = now - timedelta(days=1)
        interval = timedelta(hours=1)
        format_str = '%H:00'
    elif time_range == 'week':
        start_date = now - timedelta(weeks=1)
        interval = timedelta(days=1)
        format_str = '%a'
    elif time_range == 'month':
        start_date = now - timedelta(days=30)
        interval = timedelta(days=1)
        format_str = '%d'
    else:  # year
        start_date = now - timedelta(days=365)
        interval = timedelta(days=30)
        format_str = '%b'
    
    data = {
        'labels': [],
        'user_growth': [],
        'revenue_growth': []
    }
    current = start_date
    
    while current <= now:
        next_period = current + interval
        user_growth = calculate_growth_rate(User, current)
        revenue_growth = calculate_revenue_growth(current)
        
        data['labels'].append(current.strftime(format_str))
        data['user_growth'].append(float(user_growth))
        data['revenue_growth'].append(float(revenue_growth))
        current = next_period
    
    return data

def get_regional_data():
    """Get performance data by region"""
    regions = {}
    
    for franchise in Franchise.objects(status='active'):
        if franchise.region not in regions:
            regions[franchise.region] = {
                'revenue': 0,
                'franchises': 0,
                'performance': 0
            }
        
        regions[franchise.region]['revenue'] += float(franchise.revenue)
        regions[franchise.region]['franchises'] += 1
        regions[franchise.region]['performance'] += float(franchise.performance_score)
    
    # Calculate averages and normalize data
    max_revenue = max((r['revenue'] for r in regions.values()), default=0)
    
    normalized_data = {}
    for region, data in regions.items():
        if data['franchises'] > 0:
            avg_performance = data['performance'] / data['franchises']
            normalized_revenue = (data['revenue'] / max_revenue) * 100 if max_revenue > 0 else 0
            normalized_data[region] = (normalized_revenue + avg_performance) / 2
    
    return normalized_data
