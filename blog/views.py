from music.pagination import CustomNumberPagination
from music.utils import custom_exception_handler

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

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
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

### Blog View
class BlogClassView(GenericAPIView):
    queryset = BlogClass.objects.all()
    serializer_class = BlogClassSerializer

    @swagger_auto_schema(
        operation_summary = 'get all blog class',
        tags = ['blog'],
    )
    def get(self, request, *args, **kwargs):
        blog_classes = self.get_queryset()
        serializer = self.serializer_class(blog_classes, many = True)
        return Response(data = serializer.data, status = status.HTTP_200_OK)


class BlogPostGetView(GenericAPIView):
    queryset = BlogPost.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = BlogPostSerializer
    pagination_class = CustomNumberPagination

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
                'id',
                in_ = openapi.IN_QUERY,
                description = 'blog id',
                type = openapi.TYPE_INTEGER,
                required = False
            ),
            openapi.Parameter(
                'class',
                in_ = openapi.IN_QUERY,
                description = 'classification',
                type = openapi.TYPE_STRING,
                required = False
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page')
        self.page_size = request.GET.get('page_size')

        post_id = request.GET.get('id')

        if post_id:
            post = self.get_queryset().get(pk = post_id)
            serializer = self.serializer_class(post, many = False, context = {'detail': True})
            data = serializer.data

        else :
            posts = self.get_queryset().order_by('created_time')
            
            if request.GET.get('class'):
                classification = [int(class_x) for class_x in request.GET.get('class').split(',')]
                posts = posts.filter(blogclass_id__in = classification)
            
            pag_posts = self.paginate_queryset(posts)
            serializer = self.serializer_class(pag_posts, many = True)
            data = self.get_paginated_response(serializer.data).data
        return Response(data = data, status = status.HTTP_200_OK)
            


class BlogSearchView(GenericAPIView):
    queryset = BlogPost.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = BlogPostSerializer
    pagination_class = CustomNumberPagination


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
        posts = self.get_queryset().filter(title__contains = keyword).order_by('created_time')
        if len(posts) == 0:
            posts = BlogSection.objects.all().filter(post_type = 'text', text__contains = keyword)
        pag_posts = self.paginate_queryset(posts)
        serializer = self.serializer_class(pag_posts, many = True)
        data = self.get_paginated_response(serializer.data).data

        return Response(data = data, status = status.HTTP_200_OK)


### Manage View
class BlogPostUserGetView(GenericAPIView):
    queryset = BlogPost.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = BlogPostSerializer
    pagination_class = CustomNumberPagination
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary = 'Get personal post about music',
        tags = ['blog manage'],
        manual_parameters = [
            openapi.Parameter(
                'user_id',
                in_ = openapi.IN_QUERY,
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
            ),
            openapi.Parameter(
                'id',
                in_ = openapi.IN_QUERY,
                description = 'blog id',
                type = openapi.TYPE_INTEGER,
                required = False
            ),
            openapi.Parameter(
                description= '''
                This is a HTTP Basic authentication => https://en.wikipedia.org/wiki/Basic_access_authentication
                1. from base64 import b64encode
                2. fill this field with => Basic b64encode(b"username:password").decode("utf-8")
                ''',
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        print('user_id is =>', user_id)

        self.page = request.GET.get('page')
        self.page_size = request.GET.get('page_size')

        post_id = request.GET.get('id')

        try :
            if post_id:
                post = self.get_queryset().get(pk = post_id, user__pk = user_id)
                serializer = self.serializer_class(post, many = False, context = {'detail': True})
                data = serializer.data

            else :
                posts = self.get_queryset().filter(user__pk = user_id).order_by('created_time')
                
                if request.GET.get('class'):
                    classification = [int(class_x) for class_x in request.GET.get('class').split(',')]
                    posts = posts.filter(blogclass_id__in = classification)
                
                pag_posts = self.paginate_queryset(posts)
                serializer = self.serializer_class(pag_posts, many = True)
                data = self.get_paginated_response(serializer.data).data
            return Response(data = data, status = status.HTTP_200_OK)

        except Exception as error:
            res = 'no post match'
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)



class BlogPostManageView(GenericAPIView):
    queryset = BlogPost.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = BlogPostSerializer
    pagination_class = CustomNumberPagination
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

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
                'photo',
                in_ = openapi.IN_FORM,
                description = 'meta photo of blog post',
                type = openapi.TYPE_FILE,
                required = True
            ),
            openapi.Parameter(
                'music_sheet',
                in_ = openapi.IN_FORM,
                description = 'music sheet (pdf) of blog post',
                type = openapi.TYPE_FILE
            ),
            openapi.Parameter(
                description= '''
                This is a HTTP Basic authentication => https://en.wikipedia.org/wiki/Basic_access_authentication
                1. from base64 import b64encode
                2. fill this field with => Basic b64encode(b"username:password").decode("utf-8")
                ''',
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING
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
                description= '''
                This is a HTTP Basic authentication => https://en.wikipedia.org/wiki/Basic_access_authentication
                1. from base64 import b64encode
                2. fill this field with => Basic b64encode(b"username:password").decode("utf-8")
                ''',
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING
            )
        ]
    )
    def patch(self, request, *args, **kwargs):
        post_id = request.GET.get('id')
        post_to_update = self.get_queryset().get(pk = post_id)
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
            ),
            openapi.Parameter(
                description= '''
                This is a HTTP Basic authentication => https://en.wikipedia.org/wiki/Basic_access_authentication
                1. from base64 import b64encode
                2. fill this field with => Basic b64encode(b"username:password").decode("utf-8")
                3. Basic YW5uOmFubjEyMw==
                ''',
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING
            )
        ]
    )
    def delete(self, request, *args, **kwargs):
        post_id = request.GET.get('id') 
        post = self.get_queryset().get(pk = post_id)
        
        # delete files saved in S3 bucket
        key_list = [post.photo.name, post.music_sheet.name]
        try:
            s3 = boto3.resource('s3')
            for key in key_list:
                s3.Object(os.environ.get('AWS_STORAGE_BUCKET_NAME'), key).delete()
        except Exception as error:
            raise error

        post.delete()
        return Response(data = f'delete blog post id {post_id} successfully', status = status.HTTP_200_OK)


class BlogSectionView(GenericAPIView):
    queryset = BlogSection.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = BlogSectionSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

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
            ),
            openapi.Parameter(
                description= '''
                This is a HTTP Basic authentication => https://en.wikipedia.org/wiki/Basic_access_authentication
                1. from base64 import b64encode
                2. fill this field with => Basic b64encode(b"username:password").decode("utf-8")
                ''',
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING
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
            ),
            openapi.Parameter(
                description= '''
                This is a HTTP Basic authentication => https://en.wikipedia.org/wiki/Basic_access_authentication
                1. from base64 import b64encode
                2. fill this field with => Basic b64encode(b"username:password").decode("utf-8")
                ''',
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING
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
            ),
            openapi.Parameter(
                description= '''
                This is a HTTP Basic authentication => https://en.wikipedia.org/wiki/Basic_access_authentication
                1. from base64 import b64encode
                2. fill this field with => Basic b64encode(b"username:password").decode("utf-8")
                ''',
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING
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


