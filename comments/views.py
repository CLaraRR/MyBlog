from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Article

from .models import Comment
from .forms import CommentForm

# Create your views here.
def article_comment(request, article_id):
    article = get_object_or_404(Article, pk = article_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.article = article
            comment.save()
            return redirect(article)
        else:
            comment_list = article.comment_set.all()
            dict = {'article': article, 'form': form, 'comment_list': comment_list}
            return render(request, 'blog/single.html', dict)
    else:
        return redirect(article)







