from django.urls import path
from . import views
from .views import *
from .models import *

urlpatterns = [
    path('', views.main, name = "main"),
    path('list/', views.listt, name = "listt"),
    path('article/ <int:id>', related, name="related"),
    path('signUp/', views.signUp, name = "signUp"),
    path('logIn/', views.logIn, name = "logIn"),
    path('userpanel/', views.userpanel, name = "userpanel"),
    path('add_post/', AddPost.as_view(), name="add_post"),
    path('searched/', SearchList, name="searched"),
    path('edit<int:pk>', EditPost.as_view(model=post, success_url="userpanel"), name="editpostt"),
    path('delete<int:pk>', Deletepost.as_view(model=post, success_url="userpanel"), name="deletepostt"),
    path('comment_on_<int:pk>', Addcomment.as_view(), name="add_comment"),
    path('reply_comment_on_<int:pk> <int:pk_alt>', replycomment.as_view(), name="reply_comment"),
    path('submit_comment/<int:id>', views.submit_comment, name="submit_comment"),
    ]
