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
    product_id = serializers.SerializerMethodField()
    product_type_id = serializers.SerializerMethodField()

    def get_product_type_id(self, instance):
        if instance.product_b.all():
            return instance.product_b.all()[0].product_type.pk
        return None

    def get_product_id(self, instance):
        if instance.product_b.all():
            return instance.product_b.all()[0].pk
        return None

    def to_representation(self, instance):
        blog_post = super(BlogPostSerializer, self).to_representation(instance)

        if self.context.get('detail'):
            blog_section = BlogSectionSerializer(instance.blog_section.all().order_by('order'), many = True).data
            blog_post['blog_section'] = blog_section
        return blog_post


    class Meta:
        model = BlogPost
        fields = ('id', 'user_id', 'blogclass_id', 'title', 'description', 'photo', 'music_sheet', 'created_time', 'permission', 'product_id', 'product_type_id',)



class BlogSectionSerializer(serializers.ModelSerializer):
    blogpost_id = serializers.IntegerField()
    order = serializers.IntegerField()
    post_type = serializers.CharField()
    text = serializers.CharField(allow_null = True)
    photo_id = serializers.IntegerField(allow_null = True)
    video = serializers.CharField(allow_null = True)
    photo = serializers.SerializerMethodField()

    def get_photo(self, instance):
        if instance.photo:
            return instance.photo.image.url
        return None

    def update(self, instance, data, used_photos):
        print('data is =>', data)
        print('used_photo is =>', used_photos)
        if instance.post_type == 'photo' and instance.photo_id not in used_photos:
            print('instance.photo is =>', instance.photo)
            instance.photo.delete()
            instance.photo.save()
        instance.__dict__.update(**data)
        instance.photo_id = data.get('photo_id', None)
        instance.save()

        return instance
    class Meta:
        model = BlogSection
        fields = ('id', 'blogpost_id', 'order', 'post_type', 'text', 'photo_id', 'video', 'photo')


class ListBlogSectionSerializer(serializers.ListSerializer):
    child = BlogSectionSerializer()

    def update(self, instance, data):
        used_photos = [value for sec in data for key, value in sec.items() if key == 'photo']
        # Map for id => instance and id => data item.
        db_section = {section.order: section for section in instance}
        data_section = {section.get('order'): section for section in data}

        # Perform createions and updates.
        ret = []
        for data_order, data in data_section.items():
            section = db_section.get(data_order, None)
            if section is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(section, data, used_photos))

        # Perform deletions. If this order is not in data
        for db_order, data in db_section.items():
            if db_order not in data_section:
                data.delete()
        return ret