from django import forms

from users.models import Student, Teacher, Course, Group


class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'phone', 'group', 'avatar']


class AddTeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'phone']


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']


class AddGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'teacher', 'course', 'day', 'start_date', 'end_date', 'lesson_time']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('avatar',)
        labels = {
            'avatar': 'Аватар',  # Label in Russian
        }


class EditStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'group', 'coins', 'xp', 'avatar']


class EditTeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'phone']


class EditGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'teacher', 'course', 'day', 'start_date', 'end_date', 'lesson_time']


class EditCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']
