from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from ProjectsHub.models import Student, Instructor


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_student(sender, instance, created, **kwargs):
    if created and instance.account_type == 'student':
        Student.objects.create(user=instance, student_id=instance.username)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_instructor(sender, instance, created, **kwargs):
    if created and instance.account_type == 'instructor':
        Instructor.objects.create(user=instance)