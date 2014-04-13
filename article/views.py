from django.shortcuts import render
from django.http import HttpResponse
from article.models import Article
from django.template.loader import get_template
from django.template import Context

# Create your views here.


def home(request):
    t = get_template('list.html')
    articles = Article.all()
    html = t.render(Context({'articles': articles}))

    return HttpResponse(html)
