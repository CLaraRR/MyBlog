from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
import markdown


# Create your models here.

# class name represent table name in database
class Category(models.Model):
    name = models.CharField(max_length = 30)
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length = 30)
    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(default = 'Title', max_length = 30)
    content = models.TextField(null = True)
    create_time = models.DateTimeField(auto_now_add = True)
    modify_time = models.DateTimeField(auto_now = True)
    summary = models.CharField(max_length = 200, blank = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)  # 级联
    tags = models.ManyToManyField(Tag, blank = True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    views = models.PositiveIntegerField(default = 0, editable = False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article_page', kwargs = {'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields = ['views'])

    def save(self, *args, **kwargs):
        if not self.summary:
            md = markdown.Markdown(extensions = [
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.summary = strip_tags(md.convert(self.content))[:50]

        super(Article, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-create_time']

