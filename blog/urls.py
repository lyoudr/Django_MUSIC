from django.urls import path
from blog.views import (
    BlogClassView,
    BlogPostManageView,
    BlogPostView,
    BlogPostDetailView,
    BlogPostUserGetView,
    BlogSectionView,
    BlogSearchView
)


urlpatterns = [
    # blog view
    path('/', BlogPostView.as_view(), name = 'blog post'),
    path('<int:pk>/', BlogPostDetailView.as_view(), name = 'blog post'),
    path('class/', BlogClassView.as_view(), name = 'blog class'),
    path('search/', BlogSearchView.as_view(), name = 'search blog'),

    # manage view
    path('post/get/user', BlogPostUserGetView.as_view()),
    path('post/manage/', BlogPostManageView.as_view()),
    path('section/', BlogSectionView.as_view()),
]