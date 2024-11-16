from django.contrib import admin

from .models import Student, Teacher, Group, Course
from .views import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Group)
admin.site.register(Course)