#import
from django.urls import path
from . import views
from .models import Article
from django.views import generic # Second add
##############################################################
 
app_name = 'bbs'

#URL_名称定義
urlpatterns = [
        #index
    path('', views.IndexView.as_view(), name='index'),
        #view
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
        #criate
    path('create/', views.CreateView.as_view(), name='create'),
    #return
    path('comment/<int:pk>/', views.CommentView.as_view(), name='comment'),
    #update
    path('<int:pk>/update/', views.UpdateView.as_view(), name='update'),
        #delete
    path('<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
]