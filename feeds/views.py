from django.shortcuts import render

from .models import Feed, Article


def index(request):
    feeds = Feed.objects.all()
    for feed in feeds:
        articles = Article.objects.filter(
            feed=feed).order_by('-date_published')
        feed.article_set.set(articles, clear=True)
    return render(request, 'feeds/index.html', {'feeds': feeds})
