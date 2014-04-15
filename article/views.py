from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from article.models import Article
from django.template.loader import get_template
from django.template import Context
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from google.appengine.api import users


def _user_manage(c):
    user = users.get_current_user()
    if user is not None:
        c['username'] = user.email()
        c['logouturl'] = users.create_logout_url('/')
    else:
        c['loginurl'] = users.create_login_url()


def _require_login(wrapped_view):

    def wrap(request, *args, **kargs):
        user = users.get_current_user()
        if user is None:
            return HttpResponseRedirect('/need_login/')
        else:
            return wrapped_view(request, *args, **kargs)

    return wrap


def article_all(request):
    # Get all articles.
    articles = Article.all()
    # We order all articles from newer to older.
    articles.order('-publish_date')
    c = {'articles': articles}

    # Deal with login.
    _user_manage(c)

    # Required for the POST method form.
    c.update(csrf(request))
    c['form'] = {'action': '/article/new/'}

    return render_to_response("list.html", c)


def article_detail(request, article_id):
    # Get the article.
    article = Article.get_by_id(int(article_id))

    # Fill the context.
    c = {}
    c['article'] = article

    # Deal with login.
    _user_manage(c)

    return render_to_response("article.html", c)


@_require_login
def article_new(request):
    article = Article()
    article.title = request.POST['title']
    article.body = request.POST['new_content']
    # To be refactored once users are enabled. (Should be current user)
    article.author = users.get_current_user().email()
    article.put()

    return HttpResponseRedirect('/article/all/')


@_require_login
def article_edit(request, article_id):

    if request.method == 'GET':
        c = {}
        c.update(csrf(request))
        _user_manage(c)
        post_url = '/article/edit/' + article_id + '/'
        c['form'] = {'action': post_url}
        article = Article.get_by_id(int(article_id))
        c['article'] = article
        return render_to_response('edit_article.html', c)

    elif request.method == 'POST':
        article = Article.get_by_id(int(article_id))
        article.title = request.POST.get('title', 'untitled')
        article.body = request.POST.get('new_content', 'no content')
        article.put()
        return HttpResponseRedirect('/article/' + article_id + '/')


@_require_login
def article_delete(request, article_id):

    article = Article.get_by_id(int(article_id))
    article.delete()
    return HttpResponseRedirect('/article/all/')
