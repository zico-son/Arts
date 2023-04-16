from django.db import models
from django.conf import settings

class Level(models.Model):
    level_name = models.CharField(max_length=255)

    def __str__(self):
        return self.level_name

class Department(models.Model):
    department_name = models.CharField(max_length=255)

    def __str__(self):
        return self.department_name

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    course_code = models.CharField(max_length=255)
    course_description = models.TextField()
    course_level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='course_level')
    course_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='course_department')

    def __str__(self):
        return self.course_name

class Semester(models.Model):
    semester_name = models.CharField(max_length=255)
    year = models.IntegerField() #need to limit to 4 digits or be 22-23
    start_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
        return self.semester_name

class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor_user')
    instructor_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    def __str__(self):
        return self.instructor_name

class OpenCourse(models.Model):
    open_course_semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='open_course_semester')
    open_course_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='open_course_course')
    open_course_instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='open_course_instructor')
    open_course_capacity = models.IntegerField() # Optional

    def __str__(self):
        return self.open_course_course.course_name

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_user')
    student_name = models.CharField(max_length=255)

    def __str__(self):
        return self.student_name

class CourseRegistration(models.Model):
    course_registration_student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='course_registration_student')
    course_registration_course = models.ForeignKey(OpenCourse, on_delete=models.CASCADE, related_name='course_registration_course')

    def __str__(self):
        return self.course_registration_student.student_name


class Project(models.Model):
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()
    project_file = models.FileField(upload_to='projects/') # upload files in specific folder based on date
    project_course_registration = models.ForeignKey(CourseRegistration, on_delete=models.CASCADE, related_name='project_course_registration')

    def __str__(self):
        return self.project_name