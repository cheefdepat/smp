# myapp/templatetags/calculate_day_paused1.py

from django import template
from django.utils import timezone
from dateutil import parser

register = template.Library()

@register.filter
def days_difference(date):
    if date:
        today = timezone.now().date()
        date_obj = parser.parse(date).date()
        return (today - date_obj).days

    return None

