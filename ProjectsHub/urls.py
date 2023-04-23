from django.urls import path,include
from rest_framework.routers import DefaultRouter
from ProjectsHub.views import *



router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')
router.register('semesters', SemesterViewSet, basename='semesters')
router.register('instructors', InstructorViewSet, basename='instructors')
router.register('departments', DepartmentViewSet, basename='departments')
router.register('levels', LevelViewSet, basename='levels')
router.register('courses', CourseViewSet, basename='courses')
router.register('open-courses', OpenCourseViewSet, basename='open-courses')
urlpatterns = [
    path('', include(router.urls)),
]