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
    """Set the user information to the context c."""

    user = users.get_current_user()
    if user is not None:
        c['username'] = user.email()
        c['logouturl'] = users.create_logout_url('/')
    else:
        c['loginurl'] = users.create_login_url()


def _require_login(wrapped_view):
    """Decorator function to request login if needed."""

    def wrap(request, *args, **kargs):
        user = users.get_current_user()
        if user is None:
            return HttpResponseRedirect('/need_login/')
        else:
            return wrapped_view(request, *args, **kargs)

    return wrap


def article_all(request):
    """Shows all articles"""

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
    """Shows one article."""

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
    """Create new article, received by post."""

    # Create the article and save it.
    article = Article()
    article.title = request.POST.get('title', 'untitled')
    article.body = request.POST.get('new_content', 'no content')
    article.author = users.get_current_user().email()
    article.put()

    return HttpResponseRedirect('/article/all/')


@_require_login
def article_edit(request, article_id):
    """If the user has rights, he will be able to edit and save.
    Otherwise, he will be redirected to need_login page."""

    article = Article.get_by_id(int(article_id))

    if users.get_current_user().email() != article.author:
        return HttpResponseRedirect('/need_login/')

    else:
        if request.method == 'GET':
            c = {}
            c.update(csrf(request))
            # Give user details to template.
            _user_manage(c)
            post_url = '/article/edit/' + article_id + '/'
            # Set post url.
            c['form'] = {'action': post_url}
            # Get the article and populate the form.
            c['article'] = article

            return render_to_response('edit_article.html', c)

        elif request.method == 'POST':
            # Modify the article.
            article.title = request.POST.get('title', 'untitled')
            article.body = request.POST.get('new_content', 'no content')
            # Save it.
            article.put()

            return HttpResponseRedirect('/article/' + article_id + '/')


@_require_login
def article_delete(request, article_id):
    """We check if the user has rights to delete, and we delete."""

    article = Article.get_by_id(int(article_id))
    if users.get_current_user().email() != article.author:
        return HttpResponseRedirect('/need_login/')
    else:
        article.delete()
        return HttpResponseRedirect('/article/all/')
