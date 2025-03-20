from django.shortcuts import render,redirect, reverse

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from blo.models import Author, Category, Tag, Blog
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect




@login_required(login_url='login/')
def index(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    authors = Author.objects.all()
    blogs = Blog.objects.all()

    context = {
        'categories': categories,
        'tags': tags,
        'authors': authors,
        'blogs': blogs,
    }
    return render(request, 'index.html', context=context)
    
@login_required(login_url='login/')
def create(request):
    user = request.user
    author = Author.objects.get(user=user)
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        category = request.POST.get('category')
        description_big = request.POST.get('description_big')
        category = Category.objects.get(id=category)

        blogs = Blog.objects.create(
             title=title,
             image=image,
             description=description,
             category=category,
             description_big=description_big,
             author=author,
        )
        blogs.save()

        context = {
            'categories': categories,
            'blogs': blogs,
        }
        return redirect('blo:index')
    else:        
        context = {
            'categories': categories,
        }
        return render(request, 'create.html', context=context)

@login_required(login_url='login/')
def account(request):
    user = request.user
    author = Author.objects.get(user=user)
    blogs = Blog.objects.filter(author=author)

    context = {
        'blogs': blogs,
    }
    return render(request, 'account.html',context=context)

@login_required(login_url='login/')
def edit(request,id):
    categories = Category.objects.all()
    blogs = Blog.objects.get(id=id)

    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        category = request.POST.get('category')
        description_big = request.POST.get('description_big')
        category = Category.objects.get(id=category)

        title=title,
        image=image,
        description=description,
        category=category,
        description_big=description_big,
        author=author,     

        blogs.save()

        context = {
            'categories': categories,
            'blogs': blogs,
        }
        return redirect('blo:account')
    else:        
        context = {
            'blogs': blogs,
        }
        return render(request, 'edit.html', context=context)

@login_required(login_url='login/')
def delete(request, id):
    blogs = Blog.objects.get(id=id)
    blogs.delete()
    return redirect('blo:account')

@login_required(login_url='login/')
def blog(request,id):
    blog = Blog.objects.get(id=id)
    context = {
        'blog': blog
    }

    return render(request, 'blog.html', context=context)   

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('blo:index')
            else:
                return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')    

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'error': 'Username already exists'})
        else:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                )

        author = Author.objects.create(
            user=user
        )
        return redirect('blo:login')  
    

    else:
        return render(request, 'register.html')

@login_required(login_url='/login')
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('blo:login'))