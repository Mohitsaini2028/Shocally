from django.urls import path, include
from . import views

app_name = 'News'
urlpatterns = [

        path('', views.newsHome, name="newsHome"),
        path('newsView/<int:newsId>', views.newsView, name="newsView"),


]
