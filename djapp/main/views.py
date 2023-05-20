from django.shortcuts import render
from django.http import HttpResponseRedirect
import datetime
from . import models
from .forms import CreateNewForm, EditNewForm, SearchForm


def index(request):
    return render(request, 'index.html')


def get_news():
    posts = models.Post.objects.filter(type=models.PostType.NEW)
    nums = [num + 1 for num in range(len(posts) // 10)]
    return posts, nums

def news(request):
    posts, nums = get_news()
    return render(request, 'news.html', {'header' : 'Новости',
                                         'paginator' : nums,
                                         'post_list' : posts[:10]})

def newspaged(request, id):
    posts, nums = get_news()
    startindex = id * 10
    lastindex = (id + 1) * 10
    if lastindex > len(posts):
        lastindex = len(posts)
    print(f'startindex={startindex}, lastindex={lastindex}')
    return render(request, 'news.html', {'header' : 'Новости',
                                         'paginator' : nums,
                                         'post_list' : posts[startindex:lastindex]})


def get_articles():
    posts = models.Post.objects.filter(type=models.PostType.POST)
    nums = [num + 1 for num in range(len(posts) // 10)]
    return posts, nums


def articlespaged(request, id):
    posts, nums = get_articles()
    startindex = id * 10
    lastindex = (id + 1) * 10
    return render(request, 'articles.html', {'header' : 'Статьи',
                                         'paginator' : nums,
                                         'post_list' : posts[startindex:lastindex]})


def articles(request):
    posts, nums = get_articles()
    return render(request, 'articles.html', {'header': 'Статьи',
                                         'paginator': nums,
                                         'post_list': posts[:10]})


def new(request, id):
    return render(request, 'new.html', {'post' : models.Post.objects.get(id=id)})


def addnew(request):
    authors = models.Author.objects.all()
    form = CreateNewForm()
    form.fields['author'].choices = [(author.user.username, author.user.username) for author in authors]
    return render(request, 'addnew.html', {'form' : form})


def createnew(request):
    if request.method == 'POST':
        form = CreateNewForm(request.POST)
        author = request.POST.get('author')
        form.fields['author'].choices = [(author, author)]
        if form.is_valid():
            print(form.cleaned_data['author'])
            user = models.User.objects.get(username=form.cleaned_data['author'])
            auth = models.Author.objects.get(user=user)
            post = models.Post(author=auth, topic=form.cleaned_data['topic'], text=form.cleaned_data['text'], type=models.PostType.NEW, rating=0, date=datetime.datetime.now().isoformat())
            post.save()
        else:
            print(f'not valid {form.errors}')
    return HttpResponseRedirect('/news')


def editnew(request, pk):
    post = models.Post.objects.get(pk=pk)
    form = EditNewForm()
    form.fields['topic'].initial = post.topic
    form.fields['text'].initial = post.text
    return render(request, 'editnew.html', {'author' : post.author.user.username,
                                            'form' : form})


def do_editnew(request, pk):
    if request.method == 'POST':
        form = EditNewForm(request.POST)
        if form.is_valid():
            post = models.Post.objects.get(pk=pk)
            post.topic = form.cleaned_data['topic']
            post.text = form.cleaned_data['text']
            post.save()
    return HttpResponseRedirect('/news')

def deletenew(request, pk):
    models.Post.objects.get(pk=pk).delete()
    return HttpResponseRedirect('/news')


def article(request, id):
    return render(request, 'article.html', {'post' : models.Post.objects.get(id=id)})


def addarticle(request):
    authors = models.Author.objects.all()
    form = CreateNewForm()
    form.fields['author'].choices = [(author.user.username, author.user.username) for author in authors]
    return render(request, 'addarticle.html', {'form' : form})


def createarticle(request):
    if request.method == 'POST':
        form = CreateNewForm(request.POST)
        author = request.POST.get('author')
        form.fields['author'].choices = [(author, author)]
        if form.is_valid():
            print(form.cleaned_data['author'])
            user = models.User.objects.get(username=form.cleaned_data['author'])
            auth = models.Author.objects.get(user=user)
            post = models.Post(author=auth, topic=form.cleaned_data['topic'], text=form.cleaned_data['text'], type=models.PostType.POST, rating=0, date=datetime.datetime.now().isoformat())
            post.save()
        else:
            print(f'not valid {form.errors}')
    return HttpResponseRedirect('/articles')


def editarticle(request, pk):
    post = models.Post.objects.get(pk=pk)
    form = EditNewForm()
    form.fields['topic'].initial = post.topic
    form.fields['text'].initial = post.text
    return render(request, 'editarticle.html', {'author' : post.author.user.username,
                                            'form' : form})


def do_editarticle(request, pk):
    if request.method == 'POST':
        form = EditNewForm(request.POST)
        if form.is_valid():
            post = models.Post.objects.get(pk=pk)
            post.topic = form.cleaned_data['topic']
            post.text = form.cleaned_data['text']
            post.save()
    return HttpResponseRedirect('/articles')

def deletearticle(request, pk):
    models.Post.objects.get(pk=pk).delete()
    return HttpResponseRedirect('/articles')


def searchnews(request):
    authors = models.Author.objects.all()
    form = SearchForm()
    form.fields['author'].choices = [(author.user.username, author.user.username) for author in authors]
    return render(request, 'newssearch.html', {'form' : form})


def do_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        author = request.POST.get('author')
        form.fields['author'].choices = [(author, author)]
        if form.is_valid():
            user = models.User.objects.get(username=form.cleaned_data['author'])
            auth = models.Author.objects.get(user=user)
            topic = form.cleaned_data['topic']
            date = form.cleaned_data['date']
            print(f'author={author}, topic={topic}, date={date}')
            posts = models.Post.objects.filter(author=auth)
            if topic != '':
                posts = posts.filter(topic=topic)
            if date is not None:
                posts = posts.filter(date__gte=date)
            return render(request, 'news.html', {'header': 'Найденные новости',
                                                 'post_list': posts})
        else:
            print(form.errors)
    return HttpResponseRedirect('/')
