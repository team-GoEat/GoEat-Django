from django.template.defaulttags import register
from django import template

from django.conf import settings
import datetime

register = template.Library()

@register.filter
def version(value):

    result = settings.VERSION

    if settings.DEBUG:
        result = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    return result