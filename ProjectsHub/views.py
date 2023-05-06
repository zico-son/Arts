from rest_framework.viewsets import ModelViewSet
from ProjectsHub.customviewsets import CustomModelViewSet
from ProjectsHub.serializers import *
from ProjectsHub.models import *
from ProjectsHub.pagination import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

class ProjectViewSet(CustomModelViewSet):
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['registration__open_course__semester__semester_name']
    filterset_fields = [ 'registration__open_course__course__course_name', 'registration__open_course__semester__semester_name', 'registration__open_course__course__level__level_name','registration__open_course__course__department__department_name']
    def get_queryset(self):
        user = self.request.user
        student=Student.objects.get(user=user)
        queryset =Project.objects \
        .select_related('registration__student__user') \
        .select_related('registration__open_course__semester') \
        .select_related('registration__open_course__instructor') \
        .select_related('registration__open_course__course__level') \
        .select_related('registration__open_course__course__department')\
        .all()
        return queryset
    serializer_class = ProjectSerializer

class StudentProjectViewSet(CustomModelViewSet):
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['registration__open_course__semester__semester_name']
    filterset_fields = [ 'registration__open_course__course__course_name', 'registration__open_course__semester__semester_name', 'registration__open_course__course__level__level_name','registration__open_course__course__department__department_name']
    def get_queryset(self):
        user = self.request.user
        student=Student.objects.get(user=user)
        queryset =Project.objects \
        .select_related('registration__student__user') \
        .select_related('registration__open_course__semester') \
        .select_related('registration__open_course__instructor') \
        .select_related('registration__open_course__course__level') \
        .select_related('registration__open_course__course__department')\
        .filter(
        Q(registration__student=student)
        ).all()
        if queryset.exists():
            return queryset
        else:
            return  Project.objects.none()
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

class InstructorViewSet(CustomModelViewSet):
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
    queryset =Course.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ViewCourseSerializer
        else:
            return CreateCourseSerializer

class StudentCourseViewSet(ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['course_name', 'level__level_name', 'department__department_name']
    pagination_class = DefaultPagination
    
    def get_queryset(self):
        user = self.request.user
        student=Student.objects.get(user=user)
        queryset =Course.objects.filter(
        Q(course__open_course__student=student)
        ).all()
        if queryset.exists():
            return queryset
        else:
            return  Course.objects.none()

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

class StudentViewSet(CustomModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['student_id', 'user__first_name', 'user__last_name']
    pagination_class = DefaultPagination
    queryset = Student.objects.select_related('user').all()
    serializer_class = StudentSerializer

class CourseRegistrationViewSet(CustomModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['student__user__first_name', 'student__user__last_name']
    pagination_class = DefaultPagination
    queryset = CourseRegistration.objects.select_related('student__user').select_related('open_course__course').select_related('open_course__semester').all()
    serializer_class = CourseRegistrationSerializer

class JoinCourseViewSet(ModelViewSet):
    queryset = CourseRegistration.objects.select_related('open_course').select_related('student').all()
    serializer_class = JoinCourseSerializer
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        join_code = serializer.validated_data.get('open_course')
        open_course = get_object_or_404(OpenCourse,join_code=join_code)
        (student,created) = Student.objects.get_or_create(user=request.user)
        if created:
            student.save()
        student_name =student.user.first_name+' '+student.user.last_name
        if(CourseRegistration.objects.filter(open_course=open_course,student=student).exists()):
            return Response({"detail": "Student is already registered to this course."},status=status.HTTP_400_BAD_REQUEST)
        registration = CourseRegistration.objects.create(open_course=open_course,student=student)
        return Response({'student':student_name,'course':open_course.course.course_name})

class InstructorCourseViewSet(CustomModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['course__course_name']
    pagination_class = DefaultPagination
    serializer_class = InstructorCourseSerializer
    def get_queryset(self):
        return OpenCourse.objects.filter(instructor__user=self.request.user).select_related('course').select_related('semester').all()
    
class InstructorProjectsViewSet(CustomModelViewSet):
    filter_backends =[DjangoFilterBackend,SearchFilter]
    search_fields = ['registration__open_course__semester__semester_name']
    filterset_fields = [ 'registration__open_course__course__course_name', 'registration__open_course__semester__semester_name', 'registration__open_course__course__level__level_name','registration__open_course__course__department__department_name']
    serializer_class = ProjectSerializer
    def get_queryset(self):
        return Project.objects.filter(registration__open_course__instructor__user=self.request.user) \
                            .select_related('registration__student__user') \
                            .select_related('registration__open_course__semester') \
                            .select_related('registration__open_course__instructor') \
                            .select_related('registration__open_course__course__level') \
                            .select_related('registration__open_course__course__department')\
                            .all()