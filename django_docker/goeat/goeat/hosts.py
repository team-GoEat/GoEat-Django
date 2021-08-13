from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',

    # 유저페이지
    host(r'owner', 'app_owner.urls', name='owner'),
)