from django.contrib.auth.decorators import login_required
from django.db.transaction import commit
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.defaulttags import comment
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from blogs.forms import BlogForm
from blogs.models import Blog, Like, Comment
from users.models import Student
from django.utils import timezone
from datetime import timedelta
import json

from django.utils import timezone
from datetime import timedelta

from django.utils import timezone
from datetime import timedelta


def blogs_page(request):
    if request.method == 'POST':
        title = request.POST.get('comment')
        blog_id = request.POST.get('blog_id')
        post = Blog.objects.get(id=blog_id)
        Comment.objects.create(post=post, commenter=request.user.student, content=title)
        return redirect('blogs')

    blogs = Blog.objects.all()
    likes = Like.objects.all()
    # Faqatgina login qilgan foydalanuvchi bilan bir xil guruhdagi talabalarni filtrlash
    students = Student.objects.filter(username=request.user.username)
    group_students = Student.objects.filter(group=request.user.student.group)
    comments = Comment.objects.all()

    for comment in comments:
        comment.is_own = comment.commenter == request.user.student
        time_diff = timezone.now() - comment.created_at
        if time_diff < timedelta(hours=24):
            comment.display_time = comment.created_at.strftime('%H:%M')  # Faqat vaqtni ko'rsatish
        else:
            comment.display_time = comment.created_at.strftime('%d.%m.%Y')  # Faqat sanani ko'rsatish

    for blog in blogs:
        blog.user_liked = blog.likes.filter(liker=request.user.student).exists()

    return render(request, 'blogs.html', {'blogs': blogs, 'students': students, 'comments': comments, 'group_students': group_students, 'likes': likes})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user.student
            blog.save()
            return redirect('home')
    else:
        form = BlogForm()
    return render(request, 'create_post.html', {'form': form})


@csrf_exempt
@login_required
def like_post(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    like, created = Like.objects.get_or_create(liker=request.user.student, blog=blog)
    is_liked = created
    if not created:
        like.delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'is_liked': is_liked,
            'likes_count': blog.likes.count()
        })
    return redirect('blogs')


@csrf_exempt
@login_required
def add_comment(request, blog_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            comment_text = data.get('content')
            if comment_text:
                post = get_object_or_404(Blog, id=blog_id)
                Comment.objects.create(post=post, commenter=request.user.student, content=comment_text)
                return JsonResponse({'success': True, 'username': request.user.username, 'comment': comment_text})
            else:
                return JsonResponse({'success': False, 'error': 'Comment text is empty'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# @require_POST
# def delete_comment(request, comment_id):
#     comment = get_object_or_404(Comment, id=comment_id, commenter=request.user.student)
#     comment.delete()
#     return JsonResponse({'success': True})
def delete_comment(request, comment_id):
    # comment = get_object_or_404(Comment, id=comment_id, commenter=request.user.student)
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect('blogs')


def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user.student)
    blog.delete()
    return redirect('blogs')