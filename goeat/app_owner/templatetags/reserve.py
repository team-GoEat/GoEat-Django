from django.template.defaulttags import register
from django import template
from app_owner.views_files.reserve.callback import make_reserve

import datetime

register = template.Library()

@register.filter
def reserve_set(request, item):

    return make_reserve(request, item).content.decode('UTF-8')