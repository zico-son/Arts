from django.urls import path,include
from rest_framework.routers import DefaultRouter
from ProjectsHub.views import *
from . import views



router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')
router.register('student-projects', StudentprojectViewSet, basename='student-projects')
router.register('semesters', SemesterViewSet, basename='semesters')
router.register('instructors', InstructorViewSet, basename='instructors')
router.register('departments', DepartmentViewSet, basename='departments')
router.register('levels', LevelViewSet, basename='levels')
router.register('courses', CourseViewSet, basename='courses')
router.register('student-courses', StudentcourseViewSet, basename='student-courses')
router.register('open-courses', OpenCourseViewSet, basename='open-courses')
router.register('students', StudentViewSet, basename='students')
router.register('registrations', CourseRegistrationViewSet, basename='registrations')
router.register('join-course',JoinCourseViewSet,basename='join-course')
router.register('instructor-courses',InstructorCourseViewSet,basename='instructor-courses')
urlpatterns = [
    path('', include(router.urls)),
    
]