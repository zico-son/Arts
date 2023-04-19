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
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='level')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department')

    def __str__(self):
        return self.course_name

class Semester(models.Model):
    semester_name = models.CharField(max_length=255)
    year = models.IntegerField() #need to limit to 4 digits or be 22-23
    start_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
        return self.semester_name + ' ' + str(self.year)

class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor_user')
    title = models.CharField(max_length=255)
    def __str__(self):
        return self.title

class OpenCourse(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='semester')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='instructor')
    capacity = models.IntegerField() # Optional


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_user')
    student_id = models.CharField(max_length=255)

    def __str__(self):
        return self.student_id

class CourseRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student')
    open_course = models.ForeignKey(OpenCourse, on_delete=models.CASCADE, related_name='open_course')


class Project(models.Model):
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()
    project_file = models.FileField(upload_to='projects/') # upload files in specific folder based on date
    registration = models.ForeignKey(CourseRegistration, on_delete=models.CASCADE, related_name='registration')

    class Meta:
        ordering = ['project_name']
    def __str__(self):
        return self.project_name