import feedparser
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404

from .models import Feed, Article
from .forms import FeedForm
from .utils.news_crawler import update_feed_by_id

ARTICLES_PER_FEED = 15


def index(request):
    # TODO
    if not request.user.is_authenticated:
        messages.error(request, 'Please login or register.')
        return redirect('/feeds/login')

    model = dict()
    feeds = Feed.objects.filter(user_id=request.user.id).order_by('order')
    for feed in feeds:
        model[feed] = Article.objects.filter(
            feed=feed).order_by('date_published').reverse()[:ARTICLES_PER_FEED]

    return render(request, 'feeds/index.html', context={'model': model})


def manage(request):
    # TODO
    if not request.user.is_authenticated:
        messages.error(request, 'Please login or register.')
        return redirect('/feeds/login')

    feeds = Feed.objects.filter(user_id=request.user.id).order_by('order')

    if len(feeds) == 0:
        messages.error(request, 'No feeds registered yet.')

    return render(request, 'feeds/manage.html', context={'feeds': feeds})


def create(request):
    # TODO
    if not request.user.is_authenticated:
        messages.error(request, 'Please login or register.')
        return redirect('/feeds/login')

    if request.method == "POST":
        url = request.POST['url']
        if url:
            feed = Feed(url=request.POST['url'],
                        title=request.POST['title'],
                        website_url=request.POST['website_url'])
            try:
                d = feedparser.parse(url)
                if not feed.title:
                    feed.title = d['feed']['title']
                if not feed.website_url:
                    feed.website_url = d['feed']['link']
                feed.save()
                update_feed_by_id(feed.id)
                print(f"Saved {feed.id}")
            except Exception as e:
                raise e
            messages.success(request, f'Subscribed {feed.title}')
            return redirect('/')
        else:
            messages.error(request, 'Something wrong.')

    return render(request, 'feeds/edit.html', context={'feed': None})


def edit(request, pk):
    # TODO
    if not request.user.is_authenticated:
        messages.error(request, 'Please login or register.')
        return redirect('/feeds/login')

    if request.method == "POST":
        form = FeedForm(request.POST)
        if form.is_valid():
            feed = get_object_or_404(Feed, pk=pk)
            feed.url = request.POST['url']
            feed.title = request.POST['title']
            feed.website_url = request.POST['website_url']
            feed.order = int(request.POST['order'])
            feed.save()
            messages.success(request, f'Updated {feed}')
            return redirect('/')

    feed = get_object_or_404(Feed, pk=pk)
    return render(request, 'feeds/edit.html', context={'feed': feed})


def delete(request, pk):
    # TODO
    if not request.user.is_authenticated:
        messages.error(request, 'Please login or register.')
        return redirect('/feeds/login')

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
                messages.info(request, f'You are now logged in as {username}')
                return redirect('/')
            else:
                messages.error(request, f'Invalid username or password')
                return redirect('/feeds/login')
        else:
            messages.error(request, f'Invalid username or password')
            return redirect('/feeds/login')

    form = AuthenticationForm()
    return render(request, 'feeds/login.html', {"form": form})


def handle_logout(request):
    logout(request)
    messages.info(request, 'Logout successfull')
    return redirect('/')
