from django.http import HttpResponseNotFound
import feedparser
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest

from .models import Feed, Article
from .forms import FeedForm
from .utils.news_crawler import update_feed_by_id

import logging
logger = logging.getLogger(__name__)

ARTICLES_PER_FEED = 15

ERROR_INVALID_FEED_URL = 'Error processing request. Invalid RSS/ATOM feed URL?'
ERROR_NOT_FOUND = 'Not Found.'


@login_required(redirect_field_name=None)
def index(request):

    model = dict()
    feeds = Feed.objects.filter(user_id=request.user.id).order_by('order')
    for feed in feeds:
        model[feed] = Article.objects.filter(
            feed=feed).order_by('date_published').reverse()[:ARTICLES_PER_FEED]

    return render(request, 'feeds/index.html', context={'model': model})


@login_required
def manage(request):

    feeds = Feed.objects.filter(user_id=request.user.id).order_by('order')

    if len(feeds) == 0:
        messages.error(request, 'No feeds registered yet.')

    return render(request, 'feeds/manage.html', context={'feeds': feeds})


@login_required
def create(request):
    if request.method == "POST":
        url = request.POST['url']
        if url:
            feed = Feed(url=request.POST['url'],
                        title=request.POST['title'],
                        website_url=request.POST['website_url'])

            d = feedparser.parse(url)
            if d.status != 200:
                messages.error(request, ERROR_INVALID_FEED_URL)
                return redirect('/feeds/create')

            if not feed.title:
                feed.title = d['feed']['title']
            if not feed.website_url:
                feed.website_url = d['feed']['link']

            feed.save()
            update_feed_by_id(feed.id)

            messages.success(request, f'Subscribed to {feed}')
            return redirect('/')
        else:
            messages.error(request, 'Something wrong.')

    return render(request, 'feeds/edit.html', context={'feed': None})


@login_required
def edit(request, pk):

    try:
        feed = Feed.objects.get(pk=pk)
    except Feed.DoesNotExist:
        messages.error(request, ERROR_NOT_FOUND)
        return redirect('/feeds/')

    if request.method == "POST":
        form = FeedForm(request.POST)
        if form.is_valid():

            url = request.POST['url']

            result = feedparser.parse(url)
            if result.status != 200:
                messages.error(request, ERROR_INVALID_FEED_URL)
                return redirect(request.path)

            feed.url = url
            feed.title = request.POST['title']
            feed.website_url = request.POST['website_url']
            feed.order = int(request.POST['order'])

            feed.save()
            update_feed_by_id(feed.id)

            messages.success(request, f'Updated {feed}')
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
            print(f'User {user} created successfully')
            login(request, user)
            return redirect('/')
        else:
            # for msg in form.error_messages:
            #     print(form.error_messages[msg])
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
        return HttpResponse("Sorting!")
    else:
        return HttpResponse("Bad Request!")

