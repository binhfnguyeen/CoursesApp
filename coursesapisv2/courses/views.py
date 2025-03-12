from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response

from courses.models import Category, Course, Lesson, Tag
from courses import serializers, paginators


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = serializers.CategorySerializers
    pagination_class = paginators.ItemPaginator


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = serializers.CourseSerializers
    pagination_class = paginators.ItemPaginator

    def get_queryset(self):
        query = self.queryset
        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                query = query.filter(subjet__icontains=q)

            cate_id = self.request.query_params.get('category_id')
            if cate_id:
                query = query.filter(category_id=cate_id)

        return query

    @action(methods=['get'], detail=True, url_path='lessons')
    def get_lessons(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True)

        q = request.query_params.get('q')
        if q:
            lessons = lessons.filter(subject__icontains=q)
        return Response(serializers.LessonSerializers(lessons, many=True).data, status=status.HTTP_200_OK)


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related('tags').filter(
        active=True)  # prefetch_related trong ManyToMany thi lay du lieu can co san tranh bi tang nhieu chi phi
    serializer_class = serializers.LessonDetailsSerializer
