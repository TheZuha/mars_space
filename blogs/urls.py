from django.urls import path
from .views import like_post, add_comment, create_post, blogs_page, delete_comment, delete_blog

urlpatterns = [
    path('', blogs_page, name='blogs'),
    path('like/<int:blog_id>/', like_post, name='like_post'),
    path('add_comment/<int:blog_id>/', add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('delete_blog/<int:blog_id>/', delete_blog, name='delete_blog'),
    path('create_blog/', create_post, name='create_blog'),
]
