from rest_framework import permissions


class IsInstructor(permissions.BasePermission):
    """Allow access only to instructors."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'instructor'


class IsStudent(permissions.BasePermission):
    """Allow access only to students."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'


class IsInstructorOrReadOnly(permissions.BasePermission):
    """Instructors can write; authenticated users can read."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == 'instructor'


class IsCourseInstructor(permissions.BasePermission):
    """Only the course's own instructor can edit."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        course = getattr(obj, 'course', obj)
        return course.instructor == request.user
