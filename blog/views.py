from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Article, Category, Comment


# HOME
def home(request):
    articles = Article.objects.filter(is_approved=True)
    return render(request, 'home.html', {'articles': articles})


# REGISTER
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')

    return render(request, 'register.html')


# LOGIN
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid login")

    return render(request, 'login.html')


# ADD ARTICLE (✅ FIXED NAME)
@login_required
def add_article(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category_id = request.POST['category']

        category = Category.objects.get(id=category_id)

        Article.objects.create(
            title=title,
            content=content,
            category=category,
            author=request.user
        )

        return redirect('home')

    categories = Category.objects.all()
    return render(request, 'add_article.html', {'categories': categories})


# ARTICLE DETAIL + COMMENT
def article_detail(request, id):
    article = Article.objects.get(id=id)

    if request.method == 'POST':
        if request.user.is_authenticated:
            content = request.POST['content']

            Comment.objects.create(
                article=article,
                user=request.user,
                content=content
            )
        else:
            return redirect('login')

    comments = Comment.objects.filter(article=article)

    return render(request, 'article_detail.html', {
        'article': article,
        'comments': comments
    })
