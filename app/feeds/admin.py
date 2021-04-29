from django.contrib import admin

from .models import Feed

class FeedAdmin(admin.ModelAdmin):
    # fields = ['title', 'website_url']
    list_display = ('order', 'title', 'url', 'website_url')

admin.site.register(Feed, FeedAdmin)
