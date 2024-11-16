from django.contrib.auth.models import AbstractUser, User
from django.db import models
import random

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # related_name bilan to'qnashuv oldini olish
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set_permissions',  # related_name bilan to'qnashuv oldini olish
        blank=True
    )
# Create your models here.


    def __str__(self):
        return self.username

class Teacher(CustomUser):
    rating = models.IntegerField(default=1)
    salary = models.IntegerField(default=0)
    phone = models.CharField(max_length=13)


class Course(models.Model):
    COURSES = (
        ('Programming Backend', 'Programming Backend'),
        ('Programming Frontend', 'Programming Frontend'),
        ('Starter', 'Starter')
    )
    name = models.CharField(max_length=50, choices=COURSES)
    image = models.ImageField(upload_to='course/', blank=True, null=True)

    def __str__(self):
        return self.name

class Group(models.Model):
    DAYS = (
        ('Even', 'Even'),
        ('Odd', 'Odd'),
        ('Weekend', 'Weekend')
    )

    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher')
    day = models.CharField(max_length=10, choices=DAYS)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
    start_date = models.DateField()
    end_date = models.DateField()
    lesson_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


class Student(CustomUser):
    LIGAS = (
        ('Hacker', 'Hacker'),
        ('Coder', 'Coder'),
        ('Gamer', 'Gamer')
    )
    liga = models.CharField(max_length=10, choices=LIGAS, default=random.choice(LIGAS)[0])
    coins = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    phone = models.CharField(max_length=13, blank=True, null=True)


class Group_Student(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student')
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name} - {self.group.name}'