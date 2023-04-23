from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, StringRelatedField
from ProjectsHub.models import *


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
        fields = ['id', 'course_name','level', 'department']

class SemesterSerializer(ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'semester_name', 'year', 'start_date', 'end_date']

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
    semester = StringRelatedField()
    course = CourseSerializer()
    instructor = StringRelatedField()
    class Meta:
        model = OpenCourse
        fields = ['id','capacity','course','semester', 'instructor']

class CourseRegistrationSerializer(ModelSerializer):
    open_course = OpenCourseSerializer()
    student = StudentSerializer()
    
    class Meta:
        model = CourseRegistration
        fields = ['id', 'student', 'open_course']

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
        registration = obj.registration
        return {
            'id': registration.id,
            'course_name': registration.open_course.course.course_name,
            'level': registration.open_course.course.level.level_name,
            'department': registration.open_course.course.department.department_name,
            'semester': registration.open_course.semester.semester_name,
            'year': registration.open_course.semester.year,
        }
    def get_student(self, obj):
        registration = obj.registration 
        return {
            'id': registration.student.id,
            'student_id': registration.student.student_id,
            'first_name': registration.student.user.first_name,
            'second_name': registration.student.user.last_name
        }
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['course'] = self.get_course(instance)
        ret['student'] = self.get_student(instance)
        return ret
