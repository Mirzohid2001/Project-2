from django.shortcuts import render,redirect
from home.forms import ArticleForm

from home.models import Article

from home.forms import CommentForm

# Create your views here.

def article_func(request):
    articles = Article.objects.all()
    return render(request,'articles_list.html',{'maqolalar':articles})

def article_detail(request, slug):
    article = Article.objects.get(slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.article = article
            instance.save()
            return redirect('article_detail', slug=slug)
    form = CommentForm()
    return render(request,'article_detail.html',{'article':article})


from django.contrib.auth.decorators import login_required

@login_required(login_url='/users/sign_up')

def article_create(request):
    form = ArticleForm(request.POST or None,request.FILES)
    if request.method == 'POST' and form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        return redirect('article_func')
    form = ArticleForm()
    return render(request,'article_create.html',{'form':form})


def article_edit(request, slug):
    print(request.POST)
    article = Article.objects.get(slug=slug)
    form = ArticleForm(request.POST or None, instance=article)
    if form.is_valid():
        form.save()
        return redirect('article_detail', slug=slug)
    return render(request, 'article_edit.html',{'form':form,'article':article})

def article_delete(request, slug):
    article = Article.objects.get(slug=slug)
    if request.method == 'POST':
        article.delete()
        return redirect('article_func')
    return render(request,'article_delete.html', {'article':article})

def like_article(request, slug):
    article = Article.objects.get(slug=slug)

    if request.user not in article.likes.all():
        article.likes.add(request.user)
        article.dislikes.remove(request.user)
    elif request.user in article.likes.all():
        article.likes.remove(request.user)
    return redirect('article_detail',slug=slug)

def dislike_article(request, slug):
    article = Article.objects.get(slug=slug)

    if request.user not in article.dislikes.all():
        article.dislikes.add(request.user)
        article.likes.remove(request.user)
    elif request.user in article.dislikes.all():
        article.dislikes.remove(request.user)
    return redirect('article_detail',slug=slug)
   
    


