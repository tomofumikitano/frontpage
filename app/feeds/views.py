import json
import feedparser
from urllib.error import URLError
from xml.sax._exceptions import SAXParseException 

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .models import Feed, Article
from .forms import FeedForm
from .utils.news_crawler import update_feed_by_id, update_all_feeds

import logging
logger = logging.getLogger(__name__)

# Suppress debug message by feedpaser.parse()
# https://stackoverflow.com/questions/48429257/python-requests-module-logging-of-encoding
logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)

feedparser.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
ARTICLES_PER_FEED = 15

ERROR_INVALID_FEED_URL = 'Error processing request. Invalid RSS/ATOM feed URL?'
ERROR_FEED_URL_EXISTS = 'Error processing request. You already have the feed.'
ERROR_URL_NOT_ACCESIBLE = 'Error processing request. URL not accessible.'
ERROR_NOT_FOUND = 'Not Found.'

VALID_STATUS_CODE = [200, 301]

@login_required(redirect_field_name=None)
def index(request):
    update_all_feeds(request.user.id)

    model = dict()
    feeds = Feed.objects.filter(user_id=request.user.id).order_by('order')
    for feed in feeds:
        articles = Article.objects.filter(feed=feed)
        if feed.filter:
            for keyword in feed.filter.split(','):
                articles = articles.exclude(title__contains=keyword.strip())
        articles = articles.order_by('date_published').reverse()[:ARTICLES_PER_FEED]

        model[feed] = articles

    return render(request, 'feeds/index.html', context={'model': model})


@login_required
def manage(request):
    feeds = Feed.objects.filter(user_id=request.user.id).order_by('order')

    if len(feeds) == 0:
        messages.error(request, 'No feeds registered yet.')

    return render(request, 'feeds/manage.html', context={'feeds': feeds})


def _find_feed(url):
    d = feedparser.parse(url)
    for l in d.feed.links:
        if l.type in {'application/rss+xml', 'application/atom+xml'} and l.rel == 'alternate':
            return l.href


@login_required
def create(request):
    if request.method == "POST":
        url = request.POST['url']
        if url:
            logger.debug(f"Trying to parse {url} as RSS url ..")
            d = feedparser.parse(url)

            if d.bozo and type(d.bozo_exception) is URLError:
                logger.error(f"Error accessing url: {url}")
                messages.error(request, ERROR_URL_NOT_ACCESIBLE)
                return redirect('/feeds/create')

            if d.bozo and type(d.bozo_exception) is SAXParseException:
                # Find RSS/ATOM in URL
                logger.debug(f"Trying to parse {url} as regular url ..")
                url = _find_feed(url)
                if url:
                    logger.debug(f"Found feed URL: {url}")
                    d = feedparser.parse(url)
                else:
                    messages.error(request, ERROR_INVALID_FEED_URL)
                    return redirect('/feeds/create')

            existing_feeds = Feed.objects.filter(
                user_id=request.user.id, url=url)
            if len(existing_feeds) > 0:
                messages.error(request, ERROR_FEED_URL_EXISTS)
                return redirect('/feeds/create')

            feed = Feed(user_id=request.user.id, url=url)
            feed.title = request.POST['title'] or d['feed']['title']
            feed.website_url = request.POST['website_url'] or d['feed']['link']
            feed.filter = request.POST['filter']

            feeds = Feed.objects.filter(user_id=request.user.id)
            feed.order = 0 if len(feeds) == 0 else max(
                map(lambda feed: feed.order, feeds)) + 1
            feed.save()
            update_feed_by_id(feed.id)

            messages.success(request, f'Subscribed to {feed.title}')
            return redirect('/')
        else:
            messages.error(request, 'Hmm, something wrong. URL missing?')
            return render(request, 'feeds/edit.html', context={'feed': None})
    else:
        return render(request, 'feeds/edit.html', context={'feed': None})


@login_required
def edit(request, pk):

    try:
        feed = Feed.objects.get(pk=pk,
                                user_id=request.user.id)
    except Feed.DoesNotExist:
        messages.error(request, ERROR_NOT_FOUND)
        return redirect('/feeds/')

    if request.method == "POST":
        form = FeedForm(request.POST)
        if form.is_valid():

            url = request.POST['url']

            result = feedparser.parse(url)
            if result.status not in VALID_STATUS_CODE:
                messages.error(request, ERROR_INVALID_FEED_URL)
                return redirect(request.path)

            feed.url = url
            feed.title = request.POST['title']
            feed.website_url = request.POST['website_url']
            feed.filter = request.POST['filter']

            feed.save()
            update_feed_by_id(feed.id)

            messages.success(request, f'Updated {feed.title}')
            return redirect('/feeds/manage')

    return render(request, 'feeds/edit.html', context={'feed': feed})


@login_required
def delete(request, pk):

    if request.method == "POST":
        try:
            feed = get_object_or_404(Feed, pk=pk)
            title = feed.title
            feed.delete()
            messages.success(request, f'Deleted {title}')
        except:
            messages.error(request, 'Failed to delete')

    return redirect('/feeds/manage')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Hello {user}!')
            logger.info(f'User {user} created successfully')
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Failed creating user')
            return render(request, 'feeds/register.html', {"form": form})
    else:
        form = UserCreationForm
    return render(request, 'feeds/register.html', context={"form": form})


def handle_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Welcome back {username}!')
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('/feeds/login')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('/feeds/login')

    form = AuthenticationForm()
    return render(request, 'feeds/login.html', {"form": form})


@login_required
def handle_logout(request):
    logout(request)
    messages.info(request, 'Logout successfull')
    return redirect('/')


@login_required
def sort(request):
    if request.method == "POST":
        order = json.loads(request.body)
        feeds = Feed.objects.filter(user_id=request.user.id).order_by('order')
        for feed in feeds:
            if feed.order != order[str(feed.id)]:
                logger.debug(
                    f"{feed.title} {feed.order} -> {order[str(feed.id)]}")
                feed.order = order[str(feed.id)]
                feed.save()
        return HttpResponse("Sorted!")
    else:
        return HttpResponse("Bad Request!")
