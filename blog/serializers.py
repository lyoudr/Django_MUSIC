from django.conf import settings


from blog.models import BlogClass, BlogPost, BlogSection

from rest_framework import serializers


class BlogClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogClass
        fields = '__all__'


class BlogPostSerializer(serializers.ModelSerializer):
    blogclass_id = serializers.IntegerField()
    music_sheet = serializers.FileField(required = False)
    created_time = serializers.DateTimeField(format = settings.DATE_TIME_FORMAT, read_only=True)

    
    def to_representation(self, instance):
        blog_post = super(BlogPostSerializer, self).to_representation(instance)

        if self.context.get('detail'):
            blog_section = BlogSectionSerializer(instance.blogsection_set.all(), many = True).data
            blog_post['blog_section'] = blog_section
        return blog_post


    class Meta:
        model = BlogPost
        fields = ('id', 'user_id', 'blogclass_id', 'title', 'description', 'photo', 'music_sheet', 'created_time', 'permission')



class BlogSectionSerializer(serializers.ModelSerializer):
    blogpost_id = serializers.IntegerField()
    order = serializers.IntegerField()
    post_type = serializers.CharField()
    text = serializers.CharField(allow_null = True)
    photo = serializers.FileField(allow_null = True)
    video = serializers.CharField(allow_null = True)
    section_id = serializers.SerializerMethodField()

    def get_section_id(self, instance):
        return instance.pk
    
    class Meta:
        model = BlogSection
        fields = ('blogpost_id', 'order', 'post_type', 'text', 'photo', 'video', 'section_id')