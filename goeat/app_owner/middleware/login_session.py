from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django_hosts.resolvers import reverse
from django.http import Http404

class session_check(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        hosts = request.META['HTTP_HOST'].split('.')[0]

        if hosts == "owner":
            try:
                if request.session.get('res_id',None) is None:
                    if 'login' not in request.path and 'signup' not in request.path and 'api' not in request.path:
                        return redirect(reverse('login',host='owner'))

            except KeyError:
                request.session.clear()

                return redirect(reverse('login',host='owner'))

        response = self.get_response(request)

        return response