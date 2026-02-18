from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Course, Lesson, Assignment, Submission
from .serializers import (
    CourseSerializer, CourseListSerializer,
    LessonSerializer, AssignmentSerializer, SubmissionSerializer
)
from .permissions import IsInstructorOrReadOnly, IsCourseInstructor, IsInstructor


# ── Course Views ────────────────────────────────────────────────────────────

class CourseListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/courses/          - List all published courses
    POST /api/courses/          - Create a course (instructor only)
    """
    permission_classes = [permissions.IsAuthenticated, IsInstructorOrReadOnly]

    def get_queryset(self):
        return Course.objects.filter(is_published=True).select_related('instructor')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CourseSerializer
        return CourseListSerializer

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/courses/<id>/   - Course detail with lessons & assignments
    PUT    /api/courses/<id>/   - Update (instructor only)
    DELETE /api/courses/<id>/   - Delete (instructor only)
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourseInstructor]


class EnrollView(APIView):
    """POST /api/courses/<id>/enroll/ - Enroll/unenroll current student"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        if request.user.role != 'student':
            return Response({'detail': 'Only students can enroll.'}, status=403)
        course = get_object_or_404(Course, pk=pk, is_published=True)
        if course.students.filter(pk=request.user.pk).exists():
            course.students.remove(request.user)
            return Response({'detail': 'Successfully unenrolled from the course.'})
        course.students.add(request.user)
        return Response({'detail': 'Successfully enrolled in the course.'})


class MyCourseView(generics.ListAPIView):
    """GET /api/courses/my/ - Courses for the current user (enrolled or teaching)"""
    serializer_class = CourseListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'instructor':
            return Course.objects.filter(instructor=user)
        return user.enrolled_courses.filter(is_published=True)


# ── Lesson Views ─────────────────────────────────────────────────────────────

class LessonListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/courses/<course_id>/lessons/  - List lessons
    POST /api/courses/<course_id>/lessons/  - Add lesson (instructor only)
    """
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['course_id'])

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        if course.instructor != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only the course instructor can add lessons.')
        serializer.save(course=course)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['course_id'])


# ── Assignment Views ──────────────────────────────────────────────────────────

class AssignmentListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/courses/assignments/  - List all assignments
    POST /api/courses/assignments/  - Create assignment (instructor only)
    """
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'instructor':
            return Assignment.objects.filter(course__instructor=user)
        # Students see assignments from enrolled courses only
        return Assignment.objects.filter(course__students=user)

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if course.instructor != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only the course instructor can create assignments.')
        serializer.save()


class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Assignment.objects.all()


# ── Submission Views ──────────────────────────────────────────────────────────

class SubmissionListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/courses/submissions/  - List submissions (own, or all if instructor)
    POST /api/courses/submissions/  - Submit an assignment (student only)
    """
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'instructor':
            return Submission.objects.filter(assignment__course__instructor=user)
        return Submission.objects.filter(student=user)

    def perform_create(self, serializer):
        if self.request.user.role != 'student':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only students can submit assignments.')
        serializer.save(student=self.request.user)


class SubmissionDetailView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/courses/submissions/<id>/ - View or grade a submission"""
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'instructor':
            return Submission.objects.filter(assignment__course__instructor=user)
        return Submission.objects.filter(student=user)

    def perform_update(self, serializer):
        # Only instructors can grade
        if self.request.user.role == 'instructor':
            if 'score' in self.request.data:
                serializer.save(status='graded')
            else:
                serializer.save()
        else:
            serializer.save()
