from django.urls import path
from .views import (
    CourseListCreateView, CourseDetailView, EnrollView, MyCourseView,
    LessonListCreateView, LessonDetailView,
    AssignmentListCreateView, AssignmentDetailView,
    SubmissionListCreateView, SubmissionDetailView,
)

urlpatterns = [
    # Courses
    path('', CourseListCreateView.as_view(), name='course-list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('<int:pk>/enroll/', EnrollView.as_view(), name='course-enroll'),
    path('my/', MyCourseView.as_view(), name='my-courses'),

    # Lessons (nested under course)
    path('<int:course_id>/lessons/', LessonListCreateView.as_view(), name='lesson-list'),
    path('<int:course_id>/lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),

    # Assignments & Submissions (flat endpoints as per spec)
    path('assignments/', AssignmentListCreateView.as_view(), name='assignment-list'),
    path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),
    path('submissions/', SubmissionListCreateView.as_view(), name='submission-list'),
    path('submissions/<int:pk>/', SubmissionDetailView.as_view(), name='submission-detail'),
]
