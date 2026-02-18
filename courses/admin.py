from django.contrib import admin
from .models import Course, Lesson, Assignment, Submission


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'is_published', 'created_at']
    list_filter = ['is_published', 'instructor']
    search_fields = ['title', 'description']
    inlines = [LessonInline, AssignmentInline]
    filter_horizontal = ['students']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'created_at']
    list_filter = ['course']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'due_date', 'max_score']
    list_filter = ['course']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment', 'status', 'score', 'submitted_at']
    list_filter = ['status', 'assignment__course']
    readonly_fields = ['submitted_at', 'updated_at']
