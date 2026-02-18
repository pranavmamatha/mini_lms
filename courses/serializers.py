from rest_framework import serializers
from .models import Course, Lesson, Assignment, Submission
from accounts.serializers import UserSerializer


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'content', 'order', 'created_at']
        read_only_fields = ['created_at']


class AssignmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'course', 'course_title', 'title', 'description',
                  'due_date', 'max_score', 'created_at']
        read_only_fields = ['created_at']


class SubmissionSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'assignment_title', 'student', 'student_username',
                  'content', 'status', 'score', 'feedback', 'submitted_at', 'updated_at']
        read_only_fields = ['student', 'submitted_at', 'updated_at', 'status']


class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    assignments = AssignmentSerializer(many=True, read_only=True)
    student_count = serializers.IntegerField(source='students.count', read_only=True)
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'instructor_name',
                  'student_count', 'is_enrolled', 'lessons', 'assignments',
                  'is_published', 'created_at', 'updated_at']
        read_only_fields = ['instructor', 'created_at', 'updated_at']

    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.students.filter(pk=request.user.pk).exists()
        return False


class CourseListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for course listing."""
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)
    student_count = serializers.IntegerField(source='students.count', read_only=True)
    lesson_count = serializers.IntegerField(source='lessons.count', read_only=True)
    assignment_count = serializers.IntegerField(source='assignments.count', read_only=True)
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'instructor_name',
                  'student_count', 'lesson_count', 'assignment_count',
                  'is_enrolled', 'is_published', 'created_at']

    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.students.filter(pk=request.user.pk).exists()
        return False
