from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Article, Category, Tag
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.db.models import Q

import markdown

# Create your views here.

# def index(request):
#     articles = Article.objects.all()
#     dict = {'articles': articles}
#     return render(request, 'blog/index.html', dict)

class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}

        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False

        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data



# def article_page(request, article_id):
#     article = get_object_or_404(Article, pk = article_id)
#     article.increase_views()
#     article.content = markdown.markdown(article.content, extensions = [
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         'markdown.extensions.toc',
#     ])
#     form = CommentForm()
#     comment_list = article.comment_set.all()
#     dict = {'article': article, 'form': form, 'comment_list': comment_list}
#     return render(request, 'blog/single.html', dict)


class ArticlePageView(DetailView):
    model = Article
    template_name = 'blog/single.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        response = super(ArticlePageView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        article = super(ArticlePageView, self).get_object(queryset = None)
        md = markdown.Markdown(extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify = slugify),
        ])
        article.content = md.convert(article.content)
        article.toc = md.toc
        return article

    def get_context_data(self, **kwargs):
        context = super(ArticlePageView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list,
        })
        return context




# def archives(request, year, month):
#     articles = Article.objects.filter(create_time__year = year, create_time__month = month)
#     dict = {'articles': articles}
#     return render(request, 'blog/index.html', dict)


class ArchiveView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(create_time__year = year, create_time__month = month)


# def category(request, pk):
#     cate = Category.objects.get(pk = pk)
#     articles = Article.objects.filter(category = cate)
#     dict = {'articles': articles}
#     return render(request, 'blog/index.html', dict)

class CategoryView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk = self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category = cate)


class TagView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk = self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags = tag)


def about_page(request):
    return render(request, 'blog/about.html')


def contact_page(request):
    return render(request, 'blog/contact.html')


def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        dict = {'error_msg': error_msg}
        return render(request, 'blog/index.html', dict)

    articles = Article.objects.filter(Q(title__icontains = q) | Q(content__icontains = q))
    dict = {'error_msg': error_msg, 'articles': articles}
    return render(request, 'blog/index.html', dict)







# def edit_page(request, article_id):
#     if article_id == 0:
#         return render(request, 'blog/edit_page.html')
#     else:
#         dict = {}
#         article = Article.objects.get(id = article_id)
#         dict['article'] = article
#         return render(request, 'blog/edit_page.html', dict)
#
#
# def edit_action(request):
#     id = request.POST.get('id')
#     title = request.POST.get('title')
#     content = request.POST.get('content')
#     if id == '0':
#         # 添加文章
#         article = Article(title = title, content = content)
#         article.save()
#         dict = {}
#         dict['article'] = article
#         return render(request,'blog/article_page.html', dict)
#     else:
#         # 更新文章
#         Article.objects.filter(id = id).update(title = title, content = content)
#         dict = {}
#         article = Article.objects.get(id = id)
#         dict['article'] = article
#         return render(request, 'blog/article_page.html', dict)
