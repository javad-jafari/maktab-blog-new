from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, Comment, Category
from account.serializer import UserSerializer

User = get_user_model()


# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = '__all__'

class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    create_at = serializers.DateTimeField(read_only=True)
    update_at = serializers.DateTimeField(read_only=True)
    content = serializers.CharField(max_length=250)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    is_confirmed = serializers.BooleanField()

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.is_confirmed = validated_data.get('is_confirmed', instance.is_confirmed)
        instance.create_at = serializers.DateTimeField(read_only=True)
        instance.update_at = serializers.DateTimeField(read_only=True)
        instance.save()
        return instance


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=250)
    slug = serializers.SlugField()
    content = serializers.CharField(max_length=250)
    create_at = serializers.DateTimeField(read_only=True)
    update_at = serializers.DateTimeField(read_only=True)
    publish_time = serializers.DateTimeField(read_only=True)
    draft = serializers.BooleanField()
    image = serializers.ImageField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    author = UserSerializer(read_only=True)

    def validate(self, attrs):
        return super().validate(attrs)

    def validate_slug(self, slug):
        try:
            q = Post.objects.get(slug=slug)
            raise serializers.ValidationError("slug already is exist")
        except Post.DoesNotExist:
            return slug

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.content = validated_data.get('content', instance.content)
        instance.publish_time = validated_data.get('publish_time', instance.publish_time)
        instance.draft = validated_data.get('draft', instance.draft)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

# class CommentSerializer(serializers.ModelSerializer):
#     author_detail = UserSerializer(source='author', read_only=True)
#
#     class Meta:
#         model = Comment
#         fields = '__all__'
