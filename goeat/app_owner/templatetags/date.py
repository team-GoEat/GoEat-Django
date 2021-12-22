from django.template.defaulttags import register
from django import template

import datetime

register = template.Library()

@register.filter
def date_set(value):
    return (value + datetime.timedelta(minutes=3)).strftime('%Y-%m-%d %H:%M:%S')