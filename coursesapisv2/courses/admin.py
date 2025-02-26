from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from courses.models import Category, Course, Lesson, Tag

# Register your models here.
class LessonTagInlineAdmin(admin.TabularInline):
    model = Lesson.tags.through


class TagAdmin(admin.ModelAdmin):
    inlines = [LessonTagInlineAdmin, ]


class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'


class MyLessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'created_date', 'active', 'course']
    search_fields = ['subject']
    list_filter = ['id', 'created_date']
    readonly_fields = ['image_view']
    form = LessonForm
    inlines = [LessonTagInlineAdmin, ]

    def image_view(self, lesson):
        return mark_safe(f"<img src '/static/{lesson.image.name}' width='200' />")

    class Media:
        css = {
            'all': ('/static/CSS/style.css',)
        }


class LessonInlineAdmin(admin.StackedInline):
    model = Lesson
    fk_name = 'course'


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInlineAdmin, ]



admin.site.register(Category)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, MyLessonAdmin)
admin.site.register(Tag, TagAdmin)
