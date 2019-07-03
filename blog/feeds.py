from django.contrib.syndication.views import Feed
from .models import Article

class AllArticlesRssFeed(Feed):
    title = 'Django博客简易实现'
    link = '/'
    description = 'Django博客简易实现测试文章'

    def items(self):
        return Article.objects.all()

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):
        return item.content