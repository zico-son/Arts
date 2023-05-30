from django.db import models
from ProjectsHub.validators import semester_year_validator
from django.conf import settings
import string,random


class Level(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    description = models.TextField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='level')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department')

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Semester(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField(validators=[semester_year_validator])
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.name + ' ' + str(self.year)
    class Meta:
        ordering = ['-year']

class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor_user')
    title = models.CharField(max_length=255)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

class OpenCourse(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='semester')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='instructor')
    capacity = models.IntegerField() # Optional
    join_code = models.CharField(max_length=8,unique=1,blank=1)
    
    class Meta:
        ordering = ['course']

    def save(self, *args, **kwargs):
        if not self.join_code:
            while True:
                code =''.join(random.choices(string.ascii_lowercase+string.digits,k=8))
                if not OpenCourse.objects.filter(join_code=code).exists():
                    self.join_code = code
                    break
            super().save(*args,**kwargs)



class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_user')
    student_id = models.CharField(max_length=255)

    def __str__(self):
        return self.student_id
    class Meta:
        ordering = ['student_id']

class CourseRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student')
    open_course = models.ForeignKey(OpenCourse, on_delete=models.CASCADE, related_name='open_course')
    class Meta:
        ordering = ['student']


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='projects/') # upload files in specific folder based on date
    registration = models.ForeignKey(CourseRegistration, on_delete=models.CASCADE, related_name='registration')
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name