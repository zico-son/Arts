from rest_framework.viewsets import ModelViewSet
from ProjectsHub.serializers import *
from ProjectsHub.models import *
from ProjectsHub.pagination import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
class ProjectViewSet(ModelViewSet):
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['registration__open_course__semester__semester_name']
    filterset_fields = [ 'registration__open_course__course__course_name', 'registration__open_course__semester__semester_name', 'registration__open_course__course__level__level_name','registration__open_course__course__department__department_name']

    
    queryset = Project.objects.select_related('registration__student__user').select_related('registration__open_course__semester').select_related('registration__open_course__instructor').select_related('registration__open_course__course__level').select_related('registration__open_course__course__department').all()
    serializer_class = ProjectSerializer

class SemesterViewSet(ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.select_related('level').select_related('department').all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ViewCourseSerializer
        else:
            return CreateCourseSerializer