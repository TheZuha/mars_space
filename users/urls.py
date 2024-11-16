from django.urls import path

from users.views import login_view, admin_page, add_student, logout_view, edit_profile, add_course, add_group, \
    add_teacher, edit_student, edit_group, edit_course, edit_teacher, teacher_page, friend_page

urlpatterns = [
    path('', admin_page, name='admin_page'),
    path('login/', login_view, name='login'),
    path('teacher-dashboard/', teacher_page, name='teacher_page'),
    path('friend/<int:student_id>/', friend_page, name='friend_page'),
    path('add_student/', add_student, name='add_student'),
    path('add_teacher/', add_teacher, name='add_teacher'),
    path('add_course/', add_course, name='add_course'),
    path('add_group/', add_group, name='add_group'),
    path('edit_student/<int:id>/', edit_student, name='edit_student'),
    path('edit_teacher/<int:id>/', edit_teacher, name='edit_teacher'),
    path('edit_course/<int:id>/', edit_course, name='edit_course'),
    path('edit_group/<int:id>/', edit_group, name='edit_group'),
    path('edit_profile/<str:username>/', edit_profile, name='edit_profile'),
    path('logout/', logout_view, name='logout'),
]
