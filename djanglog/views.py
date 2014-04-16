from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from article.models import Article
from django.template.loader import get_template
from django.template import Context
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from google.appengine.api import users


def need_login(request):
    """Request for login."""
    c = {}
    c['loginurl'] = users.create_login_url()
    return render_to_response('need_login.html', c)
