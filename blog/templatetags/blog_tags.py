from ..models import Article, Category, Tag
from django import template
from django.db.models.aggregates import Count

register = template.Library()

@register.simple_tag
def get_recent_articles(num = 5):
    return Article.objects.all().order_by('-create_time')[:num]


@register.simple_tag
def archives():
    return Article.objects.dates('create_time', 'month', order = 'DESC')


@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts = Count('article')).filter(num_posts__gt = 0)


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts = Count('article')).filter(num_posts__gt = 0)
