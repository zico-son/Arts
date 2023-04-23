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
    filter_backends = [SearchFilter]
    search_fields = ['semester_name', 'year']
    pagination_class = DefaultPagination
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

class DepartmentViewSet(ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['department_name']
    pagination_class = DefaultPagination
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class LevelViewSet(ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['level_name']
    pagination_class = DefaultPagination
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

class InstructorViewSet(ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['user__first_name', 'user__last_name']
    pagination_class = DefaultPagination
    queryset = Instructor.objects.select_related('user').all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ViewInstructorSerializer
        else:
            return CreateInstructorSerializer
class CourseViewSet(ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['course_name', 'level__level_name', 'department__department_name']
    pagination_class = DefaultPagination
    queryset = Course.objects.select_related('level').select_related('department').all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ViewCourseSerializer
        else:
            return CreateCourseSerializer
        
class OpenCourseViewSet(ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['course__course_name', 'semester__semester_name', 'instructor__user__first_name', 'instructor__user__last_name']
    pagination_class = DefaultPagination
    queryset = OpenCourse.objects.select_related('course').select_related('semester').select_related('instructor').select_related('instructor__user').all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ViewOpenCourseSerializer
        else:
            return CreateOpenCourseSerializer

class StudentViewSet(ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['student_id', 'user__first_name', 'user__last_name']
    pagination_class = DefaultPagination
    queryset = Student.objects.select_related('user').all()
    serializer_class = StudentSerializer

class CourseRegistrationViewSet(ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['student__user__first_name', 'student__user__last_name']
    pagination_class = DefaultPagination
    queryset = CourseRegistration.objects.select_related('student__user').select_related('open_course__course').select_related('open_course__semester').all()
    serializer_class = CourseRegistrationSerializer