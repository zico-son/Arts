from rest_framework.serializers import ModelSerializer, StringRelatedField
from ProjectsHub.models import *
from drf_writable_nested import WritableNestedModelSerializer as NestedSerializer


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class LevelSerializer(ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'

class CourseSerializer(ModelSerializer):
    course_department = StringRelatedField()
    course_level = StringRelatedField()
    class Meta:
        model = Course
        fields = ['id', 'course_name','course_level', 'course_department']

class SemesterSerializer(ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'

class StudentSerializer(ModelSerializer):
    user = StringRelatedField()
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'user']

class InstructorSerializer(ModelSerializer):
    class Meta:
        model = Instructor
        fields = '__all__'

class OpenCourseSerializer(ModelSerializer):
    open_course_semester = StringRelatedField()
    open_course_course = CourseSerializer()
    open_course_instructor = StringRelatedField()
    class Meta:
        model = OpenCourse
        fields = ['id','open_course_capacity','open_course_course','open_course_semester', 'open_course_instructor']

class CourseRegistrationSerializer(ModelSerializer):
    course_registration_course = OpenCourseSerializer()
    course_registration_student = StudentSerializer()
    
    class Meta:
        model = CourseRegistration
        fields = ['id', 'course_registration_student', 'course_registration_course']

class ProjectSerializer(NestedSerializer):
    project_course_registration = CourseRegistrationSerializer()
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'project_description', 'project_course_registration']
        