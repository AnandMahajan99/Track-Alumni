from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.utils import timezone
from django.urls import reverse
from .models import BlogPost, PostComment, Category
from blog.forms import PostForm, CommentForm
from track_alumni.models import AlumniDetails


# Create your views here.
def index(request):
    allposts = BlogPost.objects.exclude(Published_datetime__isnull=True).order_by('-Published_datetime')
    cat = Category.objects.all()
    obj = {'post': allposts, 'cat': cat}
    # print(all)
    return render(request, 'blog/index.html', obj)


def add_post(request):
    if 'user' in request.session:
        # print(request.session['user'])
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                author = get_object_or_404(AlumniDetails, Enrollment_no=request.session['user'])
                post = form.save(commit=False)
                post.Author = author
                post.save()
                if request.POST.get('choice', '') == 'save_to_draft':
                    pass
                elif request.POST.get('choice', '') == 'post_publish':
                    p = get_object_or_404(BlogPost, Blogpost_id=post.Blogpost_id)
                    p.publish()
                return redirect('blog_home')
        else:
            form = PostForm()
        return render(request, 'blog/blogpost_form.html', {'form': form})
    return redirect('blog_home')


def post_detail(request, pid):
    post = get_object_or_404(BlogPost, Blogpost_id=pid)
    return render(request, 'blog/post_detail.html', {'post': post})


def draft_list(request):
    if 'user' in request.session:
        post = BlogPost.objects.filter(Author=request.session['user'], Published_datetime__isnull=True).order_by(
            '-Created_datetime')
        print(post)
        return render(request, 'blog/draft_list.html', {'post': post})
    return redirect('/')


def post_publish(request, pid):
    if 'user' in request.session:
        post = get_object_or_404(BlogPost, Blogpost_id=pid, Author=request.session['user'])
        post.publish()
        # print(request.path_info)
        return redirect('draft_list')
    return redirect('blog_home')


def edit_post(request, pid):
    if 'user' in request.session:
        obj = get_object_or_404(BlogPost, Blogpost_id=pid, Author=request.session['user'])
        form = PostForm(request.POST or None, instance=obj)
        if form.is_valid():
            form.save()
            if request.POST.get('choice', '') == 'save_to_draft':
                pass
            elif request.POST.get('choice', '') == 'post_publish':
                obj.publish()
            return redirect('blog_home')
        context = {'form': form}
        return render(request, 'blog/blogpost_update_form.html', context)
    return redirect('blog_home')


def delete_post(request, pid):
    if 'user' in request.session:
        post = get_object_or_404(BlogPost, Blogpost_id=pid, Author=request.session['user'])
        post.delete()
        return redirect('draft_list')
    return redirect('blog_home')


def add_new_comment(request, pid):
    if 'user' in request.session:
        if request.method == 'POST':
            user = request.session['user']
            text = request.POST.get('comment', '')
            comment = PostComment(Post_id=pid, Comment_author_id=user, Text=text, Created_datetime=timezone.now())
            comment.save()
            return redirect('post_detail', pid=pid)
    return redirect('blog_home')
