from django.db.models import Avg, Count, Case, When, F,aggregates
from django.utils import timezone

def calculate_on_time_delivery_rate(vendor):
    completed_pos = vendor.purchaseorder_set.filter(status='completed')
    total_completed = completed_pos.count()
    if total_completed == 0:
        return 0
    on_time_deliveries = completed_pos.filter(completion_date__lte=F('delivery_date')).count()
    return (on_time_deliveries / total_completed) * 100

def calculate_quality_rating_avg(vendor):
    return vendor.purchaseorder_set.filter(status='completed', quality_rating__isnull=False).aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0

def calculate_average_response_time(vendor):
    acknowledged_pos = vendor.purchaseorder_set.filter(acknowledgment_date__isnull=False)
    if not acknowledged_pos.exists():
        return 0
    return acknowledged_pos.aggregate(avg_time=Avg(F('acknowledgment_date') - F('issue_date')))['avg_time'].total_seconds() / 3600  # Convert to hours

def calculate_fulfillment_rate(vendor):
    total_pos = vendor.purchaseorder_set.count()
    if total_pos == 0:
        return 0
    fulfilled_pos = vendor.purchaseorder_set.filter(status='completed').count()
    return (fulfilled_pos / total_pos) * 100

def update_vendor_metrics(vendor):
    vendor.on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
    vendor.quality_rating_avg = calculate_quality_rating_avg(vendor)
    vendor.average_response_time = calculate_average_response_time(vendor)
    vendor.fulfillment_rate = calculate_fulfillment_rate(vendor)
    vendor.save()