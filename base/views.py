from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post, Comment, User
from .forms import PostForm, MyUserCreationForm

def home(request):
    """
    This function returns the home page with a list of posts.

    Args:
        request (HttpRequest): The incoming request.

    Returns:
        HttpResponse: The home page with a list of posts.
    """
    posts = Post.objects.all().order_by('-created')
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'base/home.html', {'page_obj': page_obj})


def about(request):
    """
    This function returns the about page.

    Args:
        request (HttpRequest): The incoming request.

    Returns:
        HttpResponse: The about page.
    """
    return render(request, 'base/about.html')


def search_view(request):
    """
    This function returns a list of posts that match the search query.

    Args:
        request (HttpRequest): The incoming request.
        query (str): The search query.

    Returns:
        HttpResponse: The search results page.
    """
    query = request.GET.get('q')
    posts = Post.objects.filter(text__icontains=query) if query else []
    context = {'posts': posts, 'query': query}
    return render(request, 'base/search_results.html', context)


def post(request, pk):
    """
    This function returns a post and its comments based on the post id.

    Args:
        request (HttpRequest): The incoming request.
        pk (int): The id of the post.

    Returns:
        HttpResponse: The post and its comments.

    """
    post = Post.objects.get(id=pk)
    post_comments = post.comment_set.all().order_by('-created')

    # creates a new comment for a post
    if request.method == 'POST':
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            text=request.POST.get('text')
        )
        return redirect('post', pk=post.id)

    context = {'post': post, 'post_comments': post_comments}
    return render(request, 'base/post.html', context)

def delete_comment(request, pk):
    """
    Delete a Comment instance.

    Args:
        request (HttpRequest): The incoming request.
        pk (int): The id of the Comment instance to be deleted.

    Returns:
        HttpResponse: A redirect to the post page.

    """
    comment = Comment.objects.get(id=pk)

    if request.method == 'POST':
        comment.delete()
        return redirect('post', pk=comment.post.id)

    context = {'object': comment}
    return render(request, 'base/delete_comment.html', context)


def create_post(request):
    """
    Create a new post.

    Args:
        request (HttpRequest): The incoming request.

    Returns:
        HttpResponse: A redirect to the home page.

    """
    form = PostForm()
    is_creating = True

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            post.user = request.user
            post.save()
            return redirect('home')

    context = {'form': form, 'is_creating': is_creating}
    return render(request, 'base/post_form.html', context)

def update_post(request, pk):
    """
    Update a post.

    Args:
        request (HttpRequest): The incoming request.
        pk (int): The id of the post to be updated.

    Returns:
        HttpResponse: A redirect to the home page.

    """
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            post.author = request.user
            post.save()
            return redirect('post', pk=post.id)
    
    context = {'form': form}
    return render(request, 'base/post_form.html', context)


def delete_post(request, pk):
    """
    Delete a Post instance.

    Args:
        request (HttpRequest): The incoming request.
        pk (int): The id of the Post instance to be deleted.

    Returns:
        HttpResponse: A redirect to the home page.

    """
    post = Post.objects.get(id=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    context = {'object': post}
    return render(request, 'base/post_delete.html', context)


def login_page(request):
    """
    This function handles the login page.

    Args:
        request (HttpRequest): The incoming request.

    Returns:
        HttpResponse: The login page.

    """
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    # Login form submission
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password incorrect')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_page(request):
    """
    Logs out the user and returns to the home page.

    Args:
        request (HttpRequest): The incoming request.

    Returns:
        HttpResponse: A redirect to the home page.

    """
    logout(request)
    return redirect('home')


def register_page(request):
    """
    This function handles the registration form.

    Args:
        request (HttpRequest): The incoming request.

    Returns:
        HttpResponse: The registration form.

    """
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, form.errors)

    context = {'form': form}
    return render(request, 'base/login_register.html', context)