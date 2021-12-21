from django.urls import path

from blog.views import (
    # Public 
    BlogClassView,
    BlogPostView,
    BlogPostDetailView,
    # User
    BlogPostUserView,
    BlogPostUserDetailView,
    BlogSectionView,
    BlogSectionManageView,
    BlogSearchView,
    # Photo
    BlogPhotoView,
)


urlpatterns = [
    # blog view
    path('', BlogPostView.as_view(), name = 'blog post'),
    path('<int:pk>', BlogPostDetailView.as_view(), name = 'blog post'),
    path('class', BlogClassView.as_view(), name = 'blog class'),
    path('search', BlogSearchView.as_view(), name = 'search blog'),

    # manage view
    path('user', BlogPostUserView.as_view(), name = 'blog post user'),
    path('user/<int:pk>', BlogPostUserDetailView.as_view(), name = 'blog post user detail'),
    path('section', BlogSectionView.as_view(), name = 'blog post section'),
    path('section/<int:pk>', BlogSectionManageView.as_view(), name = 'blog post section'),

    # photo
    path('photo', BlogPhotoView.as_view(), name = 'blog photo')
]