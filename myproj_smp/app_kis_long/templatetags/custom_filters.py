# myapp/templatetags/custom_filters.py

from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def days_difference(date):
    if date:
        today = timezone.now().date()
        return (today - date).days
    return None
