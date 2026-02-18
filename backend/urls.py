from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # API Routes
    path('api/accounts/', include('accounts.urls')),
    path('api/courses/', include('courses.urls')),
    # Frontend
    path('', TemplateView.as_view(template_name='index.html'), name='login'),
    path('courses/', TemplateView.as_view(template_name='courses.html'), name='courses'),
    path('assignments/', TemplateView.as_view(template_name='assignments.html'), name='assignments'),
]
