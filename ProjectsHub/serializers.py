from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, StringRelatedField
from ProjectsHub.models import *


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name']

class LevelSerializer(ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'level_name']

class ViewCourseSerializer(ModelSerializer):
    department = StringRelatedField()
    level = StringRelatedField()
    class Meta:
        model = Course
        fields = ['id', 'course_name','level', 'department']

class CreateCourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name','level', 'department']

class SemesterSerializer(ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'semester_name', 'year', 'start_date', 'end_date']

class StudentSerializer(ModelSerializer):
    user = serializers.SerializerMethodField() 
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'user']
    def get_user(self, obj):
        user = obj.user
        return {
            'first_name': user.first_name,
            'second_name': user.last_name,
        }

class ViewInstructorSerializer(ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Instructor
        fields = ['id', 'title', 'user'] 
    def get_user(self, obj):
        user = obj.user
        return {
            'first_name': user.first_name,
            'second_name': user.last_name,
        }
class CreateInstructorSerializer(ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id', 'title', 'user'] 


class ViewOpenCourseSerializer(ModelSerializer):
    semester = StringRelatedField()
    course = StringRelatedField()
    instructor = serializers.SerializerMethodField() 
    class Meta:
        model = OpenCourse
        fields = ['id','capacity','course','semester', 'instructor']
    def get_instructor(self, obj):
        instructor = obj.instructor
        return {
            'title': instructor.title, 
            'first_name': instructor.user.first_name,
            'second_name': instructor.user.last_name, 
        }


class CreateOpenCourseSerializer(ModelSerializer):
    class Meta:
        model = OpenCourse
        fields = ['id','capacity','course','semester', 'instructor']

class CourseRegistrationSerializer(ModelSerializer):
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
