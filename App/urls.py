from django.contrib import admin
from django.urls import path,re_path
from App import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('edit_pwd/', views.edit_pwd, name='edit-pwd'),
    path('publish/', views.publish, name='publish'),

    # 带参数的路由，显示单个帖子
    path('single/<int:tid>/', views.single, name='single'),
    path('my_admin/', views.admin, name='admin'),
    path('admin_home/', views.topic_manage, name='topic_manage'),
    path('announcement/', views.announcement, name='announcement'),
    path('kind_manage/', views.kind_manage, name='kind_manage'),
    path('single-an-<int:aid>/', views.single_an, name='single_an'),
   # path('all-<int:kid>-<int:reply_limit>-<int:time_limit>/', views.all_tie, name='all_tie'),
    # re_path(r'^all-(?P<kid>\d+)-(?P<reply_limit>\d+)-(?P<time_limit>\d+),'views.all_tie, name= 'all_tie')
    re_path(r'^all-(?P<kid>\d+)-(?P<reply_limit>\d+)-(?P<time_limit>\d+)', views.all_tie, name='all_tie'),
]
