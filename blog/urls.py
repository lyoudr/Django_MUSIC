from django.urls import path

from blog.views import (
    # Public 
    BlogClassView,
    BlogPostManageView,
    BlogPostView,
    BlogPostDetailView,
    # User
    BlogPostUserView,
    BlogSectionView,
    BlogSearchView
)


urlpatterns = [
    # blog view
    path('', BlogPostView.as_view(), name = 'blog post'),
    path('<int:pk>', BlogPostDetailView.as_view(), name = 'blog post'),
    path('class', BlogClassView.as_view(), name = 'blog class'),
    path('search', BlogSearchView.as_view(), name = 'search blog'),

    # manage view
    path('user/<int:user_id>', BlogPostUserView.as_view(), name = 'blog post user'),
    path('user', BlogPostManageView.as_view(), name = 'blog post user manage'),
    path('section/', BlogSectionView.as_view()),
]