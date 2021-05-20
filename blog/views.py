from django.db.models import Q
from django.db import transaction

from music.pagination import CustomNumberPagination

from blog.models import (
    BlogClass, 
    BlogPost, 
    BlogSection
)
from blog.serializers import (
    BlogPostSerializer, 
    BlogSectionSerializer, 
    BlogClassSerializer
)

from music.utils.custom_exception import CustomError

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import (
    FormParser,
    MultiPartParser
)

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import boto3
import os

class APICustomError(Exception): pass

### Blog View
class BlogClassView(GenericAPIView):
    queryset = BlogClass.objects.all()
    serializer_class = BlogClassSerializer
    pagination_class = CustomNumberPagination
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary = 'get all blog class',
        tags = ['blog'],
        manual_parameters = [
            openapi.Parameter(
                'page',
                in_ = openapi.IN_QUERY,
                description = 'page',
                type = openapi.TYPE_INTEGER,
                required = False
            ),
            openapi.Parameter(
                'page_size',
                in_ = openapi.IN_QUERY,
                description = 'page_size',
                type = openapi.TYPE_INTEGER,
                required = False
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page')
        self.page_size = request.GET.get('page_size')


        blog_classes = self.get_queryset()
        pg_data = self.paginate_queryset(blog_classes)
        
        if blog_classes:
            if pg_data :
                serializer = self.serializer_class(pg_data, many = True)
                data = self.get_paginated_response(serializer.data).data
                
            else:
                serializer = self.serializer_class(blog_classes, many = True)
                data = serializer.data
            
            return Response(data = data, status = status.HTTP_200_OK)    
    
        raise CustomError(
            return_code = 'can not find blog',
            return_message = 'can not find blog',
            status_code = status.HTTP_404_NOT_FOUND
        )


class BlogPostView(GenericAPIView):
    queryset = BlogPost.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = BlogPostSerializer
    pagination_class = CustomNumberPagination
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary = 'Get blog post about music',
        tags = ['blog'],
        manual_parameters = [
            openapi.Parameter(
                'page',
                in_ = openapi.IN_QUERY,
                description = 'page',
                type = openapi.TYPE_INTEGER,
                required = False
            ),
            openapi.Parameter(
                'page_size',
                in_ = openapi.IN_QUERY,
                description = 'page_size',
                type = openapi.TYPE_INTEGER,
                required = False
            ),
            openapi.Parameter(
                'class',
                in_ = openapi.IN_QUERY,
                description = 'classification',
                type = openapi.TYPE_ARRAY,
                items= openapi.Items(
                    type = openapi.TYPE_INTEGER,
                    description = 'class id'
                ),
                required = False
            )
        ]
    )
    def get(self, request):
        # page
        self.page = request.GET.get('page')
        self.page_size = request.GET.get('page_size')
        
        b_class = request.GET.get('class', None)

        posts = self.get_queryset().filter(permission = 2).order_by('created_time')
        
        if b_class:
            posts = posts.filter(blogclass_id__in = [class_x for class_x in b_class.split(',')])
        
        pag_posts = self.paginate_queryset(posts)
        serializer = self.serializer_class(pag_posts, many = True)
        data = self.get_paginated_response(serializer.data).data
        return Response(data = data, status = status.HTTP_200_OK)


class BlogPostDetailView(GenericAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        try :
            post = self.queryset.get(pk = pk)
            serializer = self.serializer_class(post)
            return Response(data = serializer.data, status = status.HTTP_200_OK)
        except BlogPost.DoesNotExist:
            raise CustomError(
                return_message = 'blog post not found', 
                return_code = 'not found', 
                status_code = status.HTTP_404_NOT_FOUND
            )


class BlogSearchView(GenericAPIView):
    queryset = BlogPost.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = BlogPostSerializer
    pagination_class = CustomNumberPagination
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary = 'keyword search blog post',
        tags = ['blog'],
        manual_parameters = [
            openapi.Parameter(
                'keyword',
                in_ = openapi.IN_QUERY,
                description = 'keyword to search',
                type = openapi.TYPE_STRING,
                required = True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        keyword = request.GET.get('keyword')
        posts = self.get_queryset().filter(
            Q(title__icontains = keyword) | 
            (Q(blog_section__post_type = 'text') & Q(blog_section__text__icontains = keyword))
        ).order_by('created_time')
        print('posts is =>', posts)
        pag_posts = self.paginate_queryset(posts)
        serializer = self.serializer_class(pag_posts, many = True)
        data = self.get_paginated_response(serializer.data).data

        return Response(data = data, status = status.HTTP_200_OK)


### Manage View
class BlogPostUserView(GenericAPIView):
    queryset = BlogPost.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = BlogPostSerializer
    pagination_class = CustomNumberPagination

    @swagger_auto_schema(
        operation_summary = 'Get personal post about music',
        tags = ['blog manage'],
        manual_parameters = [
            openapi.Parameter(
                'user_id',
                in_ = openapi.IN_PATH,
                description = 'user id',
                type = openapi.TYPE_INTEGER,
                required = True
            ),
            openapi.Parameter(
                'page',
                in_ = openapi.IN_QUERY,
                description = 'page',
                type = openapi.TYPE_INTEGER,
                required = False
            ),
            openapi.Parameter(
                'page_size',
                in_ = openapi.IN_QUERY,
                description = 'page_size',
                type = openapi.TYPE_INTEGER,
                required = False
            )
        ]
    )
    def get(self, request, user_id):
        self.page = request.GET.get('page')
        self.page_size = request.GET.get('page_size')

        posts = self.get_queryset().filter(user__pk = user_id).order_by('created_time')
        
        pag_posts = self.paginate_queryset(posts)
        serializer = self.serializer_class(pag_posts, many = True)
        data = self.get_paginated_response(serializer.data).data
        return Response(data = data, status = status.HTTP_200_OK)



class BlogPostManageView(GenericAPIView):
    queryset = BlogPost.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = BlogPostSerializer
    pagination_class = CustomNumberPagination

    @swagger_auto_schema(
        operation_summary = 'Create blog post about music',
        tags = ['blog manage'],
        manual_parameters = [
            openapi.Parameter(
                'blogclass_id',
                in_ = openapi.IN_FORM,
                description = 'blog class this post belongs to',
                type = openapi.TYPE_INTEGER,
                required = True
            ),
            openapi.Parameter(
                'title',
                in_ = openapi.IN_FORM,
                description = 'title of blog post',
                type = openapi.TYPE_STRING,
                required = True
            ),
            openapi.Parameter(
                'description',
                in_ = openapi.IN_FORM,
                description = 'description of blog post',
                type = openapi.TYPE_STRING,
                required = True
            ),
            openapi.Parameter(
                'permission',
                in_ = openapi.IN_FORM,
                description = 'private:1, public:2',
                type= openapi.TYPE_INTEGER,
                enum = [1, 2],
                required = True,
            ),
            openapi.Parameter(
                'photo',
                in_ = openapi.IN_FORM,
                description = 'meta photo of blog post',
                type = openapi.TYPE_FILE
            ),
            openapi.Parameter(
                'music_sheet',
                in_ = openapi.IN_FORM,
                description = 'music sheet (pdf) of blog post',
                type = openapi.TYPE_FILE
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data = serializer.data, status = status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_summary = 'Update blog post about music by id',
        tags = ['blog manage'],
        manual_parameters = [
            openapi.Parameter(
                'id',
                in_ = openapi.IN_QUERY,
                description = 'blog id',
                type = openapi.TYPE_INTEGER,
                required = True
            ),
            openapi.Parameter(
                'blogclass_id',
                in_ = openapi.IN_FORM,
                description = 'blog class this post belongs to',
                type = openapi.TYPE_INTEGER,
                required = True
            ),
            openapi.Parameter(
                'title',
                in_ = openapi.IN_FORM,
                description = 'title of blog post',
                type = openapi.TYPE_STRING,
                required = True
            ),
            openapi.Parameter(
                'description',
                in_ = openapi.IN_FORM,
                description = 'description of blog post',
                type = openapi.TYPE_STRING,
                required = True
            ),
            openapi.Parameter(
                'permission',
                in_ = openapi.IN_FORM,
                description = 'private:1, public:2',
                type= openapi.TYPE_INTEGER,
                enum = [1, 2],
                required = True,
            ),
            openapi.Parameter(
                'photo',
                in_ = openapi.IN_FORM,
                description = 'meta photo of blog post',
                type = openapi.TYPE_FILE
            ),
            openapi.Parameter(
                'music_sheet',
                in_ = openapi.IN_FORM,
                description = 'music sheet (pdf) of blog post',
                type = openapi.TYPE_FILE
            )
        ]
    )
    def patch(self, request):
        post_id = request.GET.get('id')
        try :
            post_to_update = self.get_queryset().get(pk = post_id)
        except BlogPost.DoesNotExist:
            raise CustomError(
                return_code = 'can not find blog',
                return_message = 'can not find blog',
                status_code = status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(
            post_to_update,
            data = request.data,
            partial = True
        )
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(data = serializer.data, status = status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_summary = 'Get blog post about music',
        tags = ['blog manage'],
        manual_parameters = [
            openapi.Parameter(
                'id',
                in_ = openapi.IN_QUERY,
                description = 'blog id',
                type = openapi.TYPE_INTEGER,
                required = True
            )
        ]
    )
    def delete(self, request, *args, **kwargs):
        post_id = request.GET.get('id') 
        try :
            post = self.get_queryset().get(pk = post_id)
        except BlogPost.DoesNotExist:
            raise CustomError(
                return_code = 'can not find blog',
                return_message = 'can not find blog',
                status_code = status.HTTP_404_NOT_FOUND
            )

        post.delete()
        return Response(data = f'delete blog post id {post_id} successfully', status = status.HTTP_200_OK)


class BlogSectionView(GenericAPIView):
    queryset = BlogSection.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = BlogSectionSerializer

    @swagger_auto_schema(
        operation_summary = 'Create blog section of music',
        tags = ['blog manage'],
        manual_parameters = [
            openapi.Parameter(
                'blogpost_id',
                in_ = openapi.IN_FORM,
                description = 'blog post id this section belongs to',
                type = openapi.TYPE_INTEGER,
                required = True
            ),
            openapi.Parameter(
                'order',
                in_ = openapi.IN_FORM,
                description = 'section order',
                type = openapi.TYPE_INTEGER,
                required = True
            ),
            openapi.Parameter(
                'post_type',
                in_ = openapi.IN_FORM,
                description = 'text, photo, video',
                type = openapi.TYPE_STRING,
                required = True
            ),
            openapi.Parameter(
                'text',
                in_ = openapi.IN_FORM,
                description = 'text content',
                type = openapi.TYPE_STRING,
                allowEmptyValue = True,
                required = True
            ),
            openapi.Parameter(
                'photo',
                in_ = openapi.IN_FORM,
                description = 'photo file',
                type = openapi.TYPE_FILE,
                allowEmptyValue = True,
                required = True
            ),
            openapi.Parameter(
                'video',
                in_ = openapi.IN_FORM,
                description = 'video file',
                type = openapi.TYPE_STRING,
                allowEmptyValue = True,
                required = True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(data = serializer.data, status = status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary = 'Update blog section of music',
        tags = ['blog manage'],
        manual_parameters = [
            openapi.Parameter(
                'section_id',
                in_ = openapi.IN_QUERY,
                description = 'section id',
                type = openapi.TYPE_INTEGER,
                required = True
            ),
            openapi.Parameter(
                'blogpost_id',
                in_ = openapi.IN_FORM,
                description = 'blog post id this section belongs to',
                type = openapi.TYPE_INTEGER,
                required = True
            ),
            openapi.Parameter(
                'order',
                in_ = openapi.IN_FORM,
                description = 'section order',
                type = openapi.TYPE_INTEGER,
                required = True
            ),
            openapi.Parameter(
                'post_type',
                in_ = openapi.IN_FORM,
                description = 'text, photo, video',
                type = openapi.TYPE_STRING,
                required = True
            ),
            openapi.Parameter(
                'text',
                in_ = openapi.IN_FORM,
                description = 'text content',
                type = openapi.TYPE_STRING,
                allowEmptyValue = True,
                required = True
            ),
            openapi.Parameter(
                'photo',
                in_ = openapi.IN_FORM,
                description = 'photo file',
                type = openapi.TYPE_FILE,
                allowEmptyValue = True,
                required = True
            ),
            openapi.Parameter(
                'video',
                in_ = openapi.IN_FORM,
                description = 'video file',
                type = openapi.TYPE_STRING,
                allowEmptyValue = True,
                required = True
            )
        ]
    )
    def patch(self, request, *args, **kwargs):
        section_id = request.GET.get('section_id')
        section_to_update = self.get_queryset().get(pk = section_id)
        serializer = self.serializer_class(
            section_to_update,
            data = request.data,
            partial = True
        )
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(data = serializer.data, status = status.HTTP_200_OK)
    

    @swagger_auto_schema(
        operation_summary = 'delete blog section',
        tags = ['blog manage'],
        manual_parameters = [
            openapi.Parameter(
                'section_id',
                in_ = openapi.IN_QUERY,
                description = 'section id',
                type = openapi.TYPE_INTEGER,
                required = True
            )
        ]
    )
    def delete(self, request, *args, **kwargs):
        section_id = request.GET.get('section_id')
        section_to_delete = self.get_queryset().get(pk = section_id)
        
        # delete files saved in S3 bucket
        if section_to_delete.post_type == 'photo':
            try :
                s3 = boto3.resource('s3')
                s3.Object(os.environ.get('AWS_STORAGE_BUCKET_NAME'), section_to_delete.photo.name).delete()
            except Exception as error:
                raise error
        
        section_to_delete.delete()
        return Response(data = f'delete blog section {section_id} successfully', status = status.HTTP_200_OK)


