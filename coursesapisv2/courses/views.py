from argparse import Action

from oauth2_provider.contrib.rest_framework import permissions
from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response

from courses.models import Category, Course, Lesson, Tag, User, Comment, Like
from courses import serializers, paginators, perms


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

    def get_permissions(self):
        if self.action in ['get_comment'] and self.request.method.__eq__('POST'):
            return [permissions.IsAuthenticated]

        return [permissions.AllowAny()]

    @action(methods=['get', 'post'], detail=True, url_path='comments')
    def get_comment(self, request, pk):
        if request.method.__eq__('POST'):
            c = serializers.CommentSerializers(data={
                'content': request.data.get('content'),
                'user': request.user.pk,
                'lesson': pk
            })
            c.is_valid(raise_exception=True)
            d = c.save()

            return Response(serializers.CommentSerializers(d).data)
        comments = self.get_object().comment_set.select_related('user').filter(active=True)
        return Response(serializers.CommentSerializers(comments, many=True).data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializers
    parser_classes = [parsers.MultiPartParser, ]
    # Không lấy dữ liệu bằng Body -> raw -> Json được
    # Lấy bằng Body -> form-data do nó là MultiPartParser

    @action(methods=['get', 'patch'], url_path='current-user', detail=False, permission_classes = [permissions.IsAuthenticated])
    def get_current_user(self, request):
        if request.method.__eq__("PATCH"):
            u = request.user

            for k, v in request.data.items():
                if k in ['first_name', 'last_name']:
                    setattr(u, k, v)
                elif k.__eq__('password'):
                    u.set_password(v)

            u.save()

            return Response(serializers.UserSerializers(u).data)

        return Response(serializers.UserSerializers(request.user).data)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.filter(active=True)
    serializers = serializers.CommentSerializers
    permission_classes = [perms.CommentOwner]