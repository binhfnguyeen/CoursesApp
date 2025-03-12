from rest_framework.serializers import ModelSerializer
from courses.models import Category, Course, Lesson, Tag

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