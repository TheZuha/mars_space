import random
from lib2to3.fixes.fix_input import context
from sqlite3 import connect

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from blogs.models import Blog
from users.forms import AddStudentForm, EditProfileForm, AddGroupForm, AddTeacherForm, AddCourseForm, EditCourseForm, \
    EditStudentForm, EditTeacherForm, EditGroupForm
from users.models import Student, Teacher

# Create your views here.


from django.shortcuts import render, redirect
from .models import Student, Teacher, Course, Group


def admin_page(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # Qidiruv qiymatini olish
            query = request.GET.get('q', '')

            # Talabalarni qidiruvga mos ravishda filtrlaymiz
            students = Student.objects.all().order_by('-date_joined')

            if query:
                students = students.filter(
                    Q(first_name__icontains=query) | Q(last_name__icontains=query)
                )

            teachers = Teacher.objects.all()
            courses = Course.objects.all()
            groups = Group.objects.all()

            context = {
                'students': students,
                'teachers': teachers,
                'courses': courses,
                'groups': groups,
            }
            return render(request, 'admin_page.html', context)
        else:
            return redirect('home')
    else:
        return redirect('login')


def add_student(request):
    if request.method == 'POST':
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            group = form.cleaned_data['group']
            avatar = form.cleaned_data['avatar']
            username = str(random.randint(100000, 999999))  # Random foydalanuvchi nomi
            password = str(random.randint(10000, 99999))  # Random parol
            print(first_name, last_name, username, password)

            # Faylga yozish (sinov uchun)
            with open('students.txt', 'a') as f:
                f.write(f"{first_name}, {last_name}, {username}, {password}, {group}\n")

            # Foydalanuvchini yaratish
            user = Student.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                               phone=phone, group=group, password=password, avatar=avatar)

            # Parolni qayta hash qilmaslik kerak
            user.save()

            return redirect('admin_page')
    else:
        form = AddStudentForm()
    return render(request, 'add_student.html', {'form': form})


def add_teacher(request):
    if request.method == 'POST':
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            username = phone
            password = f"12345{first_name}"
            user = Teacher.objects.create(username=username, first_name=first_name, last_name=last_name, phone=phone,
                                          password=password)
            user.set_password(password)
            user.save()
            return redirect('admin_page')
    else:
        form = AddTeacherForm()
    return render(request, 'add_student.html', {'form': form})


def add_course(request):
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = AddCourseForm()
    return render(request, 'add_student.html', {'form': form})


def add_group(request):
    if request.method == 'POST':
        form = AddGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = AddGroupForm()  # Re-render form with errors if not valid
    return render(request, 'add_student.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)

            # Foydalanuvchi o'qituvchi ekanligini tekshirish
            if hasattr(user, 'teacher'):  # Bu yerda O'qituvchi modelida OneToOne munosabati bor deb faraz qilamiz
                return redirect('teacher_page')  # O'qituvchilar sahifasiga yo'naltirish
            elif user.is_superuser:
                return redirect('admin_page')  # Administrator sahifasiga yo'naltirish
            else:
                return redirect('home')  # Oddiy foydalanuvchilar uchun bosh sahifaga yo'naltirish
        else:
            messages.error(request,
                           'Kirish ma\'lumotlari noto‘g‘ri')  # Kirish muvaffaqiyatsiz bo'lsa xato xabarini ko'rsatish
    return render(request, 'login.html')


def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = EditStudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = EditStudentForm(instance=student)
    return render(request, 'edit_student.html', {'form': form})


def edit_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    if request.method == 'POST':
        form = EditTeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = EditTeacherForm(instance=teacher)
    return render(request, 'edit_teacher.html', {'form': form})


def edit_group(request, id):
    group = get_object_or_404(Group, id=id)
    if request.method == 'POST':
        form = EditGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = EditGroupForm(instance=group)
    return render(request, 'edit_group.html', {'form': form})


def edit_course(request, id):
    item = "Course"
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        form = EditCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = EditCourseForm(instance=course)
    return render(request, 'edit_course.html', {'form': form, 'item': item})


def logout_view(request):
    logout(request)
    return redirect('login')


def edit_profile(request, username):
    student = get_object_or_404(Student, username=username)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш аватар успешно изменён!')
            return redirect('home')
    else:
        form = EditProfileForm(instance=student)

    return render(request, 'edit_avatar.html', {'form': form})



@csrf_exempt
def teacher_page(request):
    if request.user.is_authenticated:
        groups = Group.objects.filter(teacher=request.user)

        group_id = request.GET.get('group_id')

        if not group_id and groups.exists():
            group_id = groups.first().id

        selected_group = None
        students = None

        if request.method == 'POST':
            coins = int(request.POST.get('coins', 0))
            s_id = request.POST.get('s_id')
            if coins > 0:
                student = Student.objects.get(id=s_id)
                student.coins += coins
                student.save()

        if group_id:
            selected_group = get_object_or_404(Group, id=group_id)
            students = Student.objects.filter(group=selected_group)

        context = {
            'groups': groups,
            'selected_group': selected_group,
            'students': students,
        }
        return render(request, 'teacher_page.html', context=context)
    else:
        return redirect('login')


def friend_page(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    blogs = Blog.objects.filter(author=student)
    return render(request, 'friend_page.html', {'student': student, 'blogs': blogs})
