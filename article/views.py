from django.shortcuts import render
from django.http import HttpResponse
from article.models import Article
from django.template.loader import get_template
from django.template import Context

# Create your views here.


def article_all(request):
    t = get_template('list.html')
    articles = Article.all()
    html = t.render(Context({'articles': articles}))

    return HttpResponse(html)


def article_detail(request, article_id):
    t = get_template('article.html')
    article = Article.get_by_id(int(article_id))
    html = t.render(Context({'article': article}))

    return HttpResponse(html)
