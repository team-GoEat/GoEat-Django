from django.template.defaulttags import register
from django import template

from django.conf import settings
import datetime

register = template.Library()

@register.filter
def split(value):
    
    try:
        return value.split('-')[2]
    except:

        print(value)
        return '0000'
