from rest_framework.viewsets import ModelViewSet
from ProjectsHub.serializers import *
from ProjectsHub.models import *
from ProjectsHub.pagination import *
from django_filters.rest_framework import DjangoFilterBackend
class ProjectViewSet(ModelViewSet):
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [ 'registration__open_course__course__course_name', 'registration__open_course__semester__semester_name', 'registration__open_course__course__level__level_name','registration__open_course__course__department__department_name']

    
    queryset = Project.objects.select_related('registration__student__user').select_related('registration__open_course__semester').select_related('registration__open_course__instructor').select_related('registration__open_course__course__level').select_related('registration__open_course__course__department').all()
    serializer_class = ProjectSerializer