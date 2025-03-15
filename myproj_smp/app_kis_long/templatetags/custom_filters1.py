# app_kis_long/templatetags/custom_filters1.py
import sys
sys.path.insert(0, 'C:/Users/TurchinMV/PycharmProjects/smp/myproj_smp')
# C:\Users\TurchinMV\PycharmProjects\smp\myproj_smp
from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def days_difference(date):
    if date:
        today = timezone.now().date()
        return (today - date).days
    return None
