from rest_framework import serializers
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

class ProjectSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'attachment', 'course', 'student']
    
    name = serializers.CharField(max_length=255, source='project_name')
    description = serializers.CharField(source='project_description')
    attachment = serializers.FileField(source='project_file')

    def get_course(self, obj):
        registration = obj.project_course_registration
        return {
            'id': registration.id,
            'course_name': registration.course_registration_course.open_course_course.course_name,
            'course_level': registration.course_registration_course.open_course_course.course_level.level_name,
            'course_department': registration.course_registration_course.open_course_course.course_department.department_name,
            'semester': registration.course_registration_course.open_course_semester.semester_name,
            'year': registration.course_registration_course.open_course_semester.year,
        }
    def get_student(self, obj):
        registration = obj.project_course_registration
        return {
            'id': registration.course_registration_student.id,
            'student_id': registration.course_registration_student.student_id,
            'first_name': registration.course_registration_student.user.first_name,
            'second_name': registration.course_registration_student.user.last_name
        }
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['course'] = self.get_course(instance)
        ret['student'] = self.get_student(instance)
        return ret
