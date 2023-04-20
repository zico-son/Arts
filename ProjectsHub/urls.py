from django.urls import path,include
from rest_framework.routers import DefaultRouter
from ProjectsHub.views import *



router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')
router.register('opencourse',OpenCourseViewSet,basename='opencourse')

urlpatterns = [
    path('', include(router.urls)),
]