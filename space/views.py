from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import News
from users.models import Student


# Create your views here.

@login_required(login_url='/users/login/')
def home_view(request):
    if request.user.is_authenticated:
        students = Student.objects.filter(
            username=request.user.username)  # Login qilgan talabaning ma'lumotlarini olish
        news = News.objects.all()
        context = {'news': news, 'students': students}
        return render(request, 'home.html', context=context)
    else:
        return redirect('login')
