from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
# comment 추가
from .models import Blog, Comment
from .forms import NewBlog, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth



# 추가하고, url도 추가
def del_comment(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    comment.delete()
    return redirect('home')

 # 댓글 수정  
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment.save()
            return redirect('home')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'funccrud/add_comment.html', {'form': form})

def welcome(request):
    return render(request, 'funccrud/index.html')

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            auth.login(request, user)
            return redirect('home')
    return render(request, 'funccrud/signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'funccrud/login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'funccrud/login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

def read(request):
    blogs = Blog.objects.all()
    
    # 필터링, 정렬
    blog_list = Blog.objects.all().filter(category='과제').order_by('-created_date')
    # 페이지네이션
    paginator = Paginator(blog_list, 4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'funccrud/funccrud.html', {'blogs':blogs, 'posts':posts})

def detail(request, pk):
    blog_detail = get_object_or_404(Blog, pk=pk)
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = blog
            comment.save()
            return redirect('detail', pk)
    else:
        form = CommentForm()
    return render(request, 'funccrud/detail.html', {'blog': blog_detail, 'form': form})

# def add_comment(request, pk):
#     blog = get_object_or_404(Blog, pk=pk)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = blog
#             comment.save()
#             return redirect('home')
#     else:
#         form = CommentForm()
#     return render(request, 'funccrud/add_comment.html', {'form': form})


@login_required(login_url='/login/')
def create(request):
    if request.method == 'POST':
        form = NewBlog(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.create_date = timezone.now()
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = NewBlog()
        return render(request, 'funccrud/new.html', {'form':form})

@login_required(login_url='/login/')
def update(request, pk):
    blog = get_object_or_404(Blog, pk = pk)
    if request.method == "POST":
        form = NewBlog(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
       form = NewBlog(instance=blog) 
    return render(request, 'funccrud/new.html', {'form':form})

@login_required(login_url='/login/')
def delete(request, pk):
    blog = get_object_or_404(Blog, pk = pk)
    blog.delete()
    return redirect('home')
