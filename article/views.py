from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from article.models import Article
from django.template.loader import get_template
from django.template import Context
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

# Create your views here.


def article_all(request):
    # Get all articles.
    articles = Article.all()
    # We order all articles from newer to older.
    articles.order('-publish_date')
    c = {'articles': articles}
    # Required for the POST method form.
    c.update(csrf(request))

    return render_to_response("list.html", c)


def article_detail(request, article_id):
    t = get_template('article.html')
    article = Article.get_by_id(int(article_id))
    html = t.render(Context({'article': article}))

    return HttpResponse(html)


def article_new(request):
    article = Article()
    article.title = request.POST['title']
    article.body = request.POST['new_content']
    # To be refactored once users are enabled. (Should be current user)
    article.author = 'GCardona'
    article.put()

    return HttpResponseRedirect('/article/all/')
