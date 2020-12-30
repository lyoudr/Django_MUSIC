from django.urls import path
from blog.views import (
    BlogClassView,
    BlogPostManageView,
    BlogPostGetView,
    BlogSectionView,
    BlogSearchView,
)


urlpatterns = [
    path('class/', BlogClassView.as_view()),
    path('post/manage/', BlogPostManageView.as_view()),
    path('post/get/', BlogPostGetView.as_view()),
    path('section/', BlogSectionView.as_view()),
    path('search/', BlogSearchView.as_view())
]