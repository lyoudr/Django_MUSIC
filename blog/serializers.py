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

        # products
        products = instance.product_b.all()
        user_id = self.context.get('user_id', None)
        if products:
            is_show = products[0].owner_id != user_id and user_id
            blog_post.update({
                'product_id': products[0].pk if is_show else None,
                'product_type_id': products[0].product_type.pk if is_show else None,
            })
                
        if self.context.get('detail'):
            blog_section = BlogSectionSerializer(instance.blog_section.all().order_by('order'), many = True).data
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
    photo_id = serializers.IntegerField(allow_null = True)
    video = serializers.CharField(allow_null = True)
    photo = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_photo(self, instance):
        print('instance.pk is =>', instance.pk)
        if instance.photo_id and instance.post_type == 'photo':
            return instance.photo.image.url
        return None

    def get_name(self, instance):
        if instance.photo_id and instance.post_type == 'photo':
            return instance.photo.image.name.split('/')[1]
        return None

    def update(self, instance, data, used_photos):
        print('used_photos is =>', used_photos)
        if instance.post_type == 'photo' and instance.photo_id not in used_photos:
            instance.photo.delete()
            instance.photo.save()
        instance.__dict__.update(**data)
        instance.photo_id = data.get('photo_id', None)
        instance.save()

        return instance
    class Meta:
        model = BlogSection
        fields = ('id', 'blogpost_id', 'order', 'post_type', 'text', 'photo_id', 'video', 'photo', 'name')


class ListBlogSectionSerializer(serializers.ListSerializer):
    child = BlogSectionSerializer()

    def update(self, instance, data):
        used_photos = []
        for sec in data:
            for k, v in sec.items():
                print('k is =>', k)
                print('v is =>', v)
                if k == 'photo_id' and v:
                    used_photos.append(v)

        print('used_photos is =>', used_photos)
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