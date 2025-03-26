from rest_framework.serializers import ModelSerializer
from courses.models import Category, Course, Lesson, User, Tag, Comment

class CategorySerializers(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ItemSerializer(ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.image:
            data['image'] = instance.image.url
        return data


class CourseSerializers(ItemSerializer):
    class Meta:
        model = Course
        fields = ['id', 'subject', 'created_date', 'image', 'category_id']


class LessonSerializers(ItemSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'created_date', 'image', 'course_id']


class TagSerializers(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonDetailsSerializer(LessonSerializers):
    tags = TagSerializers(many=True)

    class Meta:
        model = LessonSerializers.Meta.model
        fields = LessonSerializers.Meta.fields + ['content', 'tags']


class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.avatar:
            data['avatar'] = instance.avatar.url
        return data

    def create(self, validated_data):
        data = validated_data.copy()
        u = User(**data)
        u.set_password(u.password)
        u.save()

        return u


class CommentSerializers(ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserSerializers(instance.user).data

        return data

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_date']
        extra_kwargs = {
            'lesson': {
                'write_only': True
            }
        }