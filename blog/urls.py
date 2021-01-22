from django.urls import path
from blog import views

urlpatterns = [
    path('', views.index, name='blog_home'),
    path('post/add', views.add_post, name='add_post'),
    path('post/publish/<int:pid>', views.post_publish, name='publish_post'),
    path('post/detail/<int:pid>', views.post_detail, name='post_detail'),
    path('post/draft', views.draft_list, name='draft_list'),
    path('post/edit/<int:pid>', views.edit_post, name='edit_post'),
    path('post/delete/<int:pid>', views.delete_post, name='delete_post'),
    path('post/comment/add/<int:pid>', views.add_new_comment, name='add_comment'),
]
