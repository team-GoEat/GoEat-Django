from django.template.defaulttags import register
from django import template

import datetime

register = template.Library()

@register.filter
def phone_slice(value):
    return value[-4:]