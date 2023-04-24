from rest_framework.viewsets import ModelViewSet
from ProjectsHub.serializers import *
from ProjectsHub.models import *
from ProjectsHub.pagination import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status

class ProjectViewSet(ModelViewSet):
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [ 'registration__open_course__course__course_name', 'registration__open_course__semester__semester_name', 'registration__open_course__course__level__level_name','registration__open_course__course__department__department_name']

    
    queryset = Project.objects.select_related('registration__student__user').select_related('registration__open_course__semester').select_related('registration__open_course__instructor').select_related('registration__open_course__course__level').select_related('registration__open_course__course__department').all()
    serializer_class = ProjectSerializer


class OpenCourseViewSet(ModelViewSet):
    queryset = OpenCourse.objects.select_related('semester').select_related('course').select_related('instructor').all()
    serializer_class = OpenCourseSerializer

class CourseEnrollmentViewSet(ModelViewSet):
    queryset = CourseRegistration.objects.select_related('open_course').select_related('student').all()
    serializer_class = CourseEnrolmentSerializer
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course_code_data = serializer.validated_data.get('open_course')
        open_course = get_object_or_404(OpenCourse,open_course_code=course_code_data)
        student = serializer.validated_data.get('student')
        registeration = CourseRegistration.objects.create(open_course=open_course,student=student)
        if(CourseRegistration.objects.filter(open_course=open_course,student=student).exists()):
           return Response({"detail": "Student is already registered to this course."},status=status.HTTP_400_BAD_REQUEST)
        return registeration


   

   
