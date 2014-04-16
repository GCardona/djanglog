from django.shortcuts import render_to_response
from google.appengine.api import users


def need_login(request):
    """Request for login."""
    c = {}
    c['loginurl'] = users.create_login_url()
    return render_to_response('need_login.html', c)
