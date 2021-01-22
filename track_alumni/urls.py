from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index, name='home'),
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('post/',views.post, name='post'),
    path('contact/',views.contact, name='contact'),
    path('about/',views.about, name='about'),
    path('profile/', views.view_profile, name='view_profile'),
    path('group/',views.group, name='group'),
    path('groupview/<int:id>',views.groupview, name='groupview'),
    path('comment/<int:id>',views.comment, name='comments'),
    path('group/new/',views.create_new_group, name='create_new_group'),
    path('group/delete/<int:gid>', views.delete_group, name='delete_group'),
    path('group/add/member/<int:gid>', views.add_group_member, name='add_member'),
    path('group/exit/<int:gid>', views.exit_group, name='exit_group'),
    path('post/new/<int:gid>',views.create_new_post, name='create_new_post'),
    #path('post_form/<int:id>',views.newpost, name='new_post'),
    path('comment/add/<int:id>', views.comment, name='add_comment'),
    path('request/', views.request_and_notifications, name='request_and_notifications'),
    path('request/send/<int:gid>/<str:id>', views.send_request, name='send_request'),
    path('request/approve/<int:rid>', views.approve_join_group_request, name='join_group'),
    path('request/delete/<int:rid>', views.delete_join_group_request, name='delete_request'),
]
