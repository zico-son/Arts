from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, StringRelatedField
from ProjectsHub.models import *
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class InstructorCourseSerializer(ModelSerializer):
    course = serializers.SerializerMethodField()
    class Meta:
        model = OpenCourse
        fields = ['join_code','course',]
    def get_course(self, obj):
        course = obj.course
        return {
            'id' : course.id,
            'name' : course.name,
            'level' : course.level.name,
            'department': course.department.name,
        }


class JoinCourseSerializer(ModelSerializer):
    student = serializers.SerializerMethodField(read_only=True)
    open_course = serializers.CharField(max_length=8)
    class Meta:
        model = CourseRegistration
        fields = ['student','open_course']
    def get_student(self, obj):
        student = obj.student
        return {
            'first_name': student.user.first_name,
            'second_name': student.user.last_name,
        }


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

class LevelSerializer(ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name']
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
class ViewCourseSerializer(ModelSerializer):
    department = StringRelatedField()
    level = StringRelatedField()
    class Meta:
        model = Course
        fields = ['id', 'name','description', 'code','level', 'department']

class CreateCourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name','description', 'code','level', 'department']

class SemesterSerializer(ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'name', 'year', 'start_date', 'end_date']



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
        fields = ['id','capacity','course', 'join_code','semester', 'instructor']
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
    student = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField() 
    class Meta:
        model = CourseRegistration
        fields = ['id', 'student', 'course']
    def get_student(self, obj):
        student= obj.student 
        return {
            'id': student.id,
            'first_name': student.user.first_name,
            'second_name': student.user.last_name
        }
    def get_course(self, obj):
        open_course = obj.open_course
        return {
            'id':open_course.id,
            'name': open_course.course.name,
            'level': open_course.course.level.name,
            'department':open_course.course.department.name,
            'semester':open_course.semester.name,
            'year':open_course.semester.year,
        }

class ProjectSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'attachment', 'course', 'student']
    
    attachment = serializers.FileField(source='file')

    def get_course(self, obj):
        registration = obj.registration
        return {
            'id': registration.id,
            'name': registration.open_course.course.name,
            'level': registration.open_course.course.level.name,
            'department': registration.open_course.course.department.name,
            'semester': registration.open_course.semester.name,
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

class StudentCoursesSerializer(ModelSerializer):
    course_info = serializers.SerializerMethodField()
    class Meta:
        model = CourseRegistration
        fields = ['course_info']
    def get_course_info(self, obj):
        open_course = obj.open_course
        return {
            'course_id':open_course.course.id,
            'course': open_course.course.name,
            'level': open_course.course.level.name,
            'department':open_course.course.department.name,
            'semester':open_course.semester.name,
            'year':open_course.semester.year,
            'instructor': open_course.instructor.user.first_name + ' ' + open_course.instructor.user.last_name,
        }
class StudentProjectsSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'attachment']
    
    attachment = serializers.FileField(source='file')

class StudentPostProjectSerializer(ModelSerializer):
    registration = serializers.CharField(max_length=8)
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'file', 'registration']
    def create(self, validated_data):
        registration = validated_data.pop('registration')
        registration = get_object_or_404(CourseRegistration, pk=registration)
        project = Project.objects.create(**validated_data, registration=registration)
        return project