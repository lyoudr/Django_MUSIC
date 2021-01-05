from django.urls import path
from blog.views import (
    BlogClassView,
    BlogPostManageView,
    BlogPostGetView,
    BlogPostUserGetView,
    BlogSectionView,
    BlogSearchView,
)


urlpatterns = [
    # blog view
    path('class/', BlogClassView.as_view()),
    path('post/get/all', BlogPostGetView.as_view()),
    path('search/', BlogSearchView.as_view()),

    # manage view
    path('post/get/user', BlogPostUserGetView.as_view()),
    path('post/manage/', BlogPostManageView.as_view()),
    path('section/', BlogSectionView.as_view()),
]