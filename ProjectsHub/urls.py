from django.urls import path,include
from rest_framework.routers import DefaultRouter
from ProjectsHub.views import *



router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')
router.register('semesters', SemesterViewSet, basename='semesters')

urlpatterns = [
    path('', include(router.urls)),
]