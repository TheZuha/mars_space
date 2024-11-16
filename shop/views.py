from django.shortcuts import render, redirect
from shop.models import Products, Shop_history
from users.models import Student


# Create your views here.


def shop_view(request):
    producs = Products.objects.all()
    students = Student.objects.filter(username=request.user.username)
    user_coins = request.user.student.coins if request.user.is_authenticated else 0
    context = {'products': producs, 'students': students, 'user_coins': user_coins}
    return render(request, 'shop.html', context)


def shop_history_view(request):
    students = Student.objects.filter(username=request.user.username)
    shop_history = Shop_history.objects.filter(buyer=request.user)
    context = {'shop_history': shop_history, 'students': students}
    return render(request, 'shop_history.html', context)


def detail_product(request, id):
    product = Products.objects.get(id=id)
    user = Student.objects.get(username=request.user.username)

    # Mahsulotni sotib olishga yetarli tangalar mavjudligini tekshirish
    if user.coins >= product.price:
        context = {'product': product, 'user': user, 'can_buy': True}
    else:
        context = {'product': product, 'user': user, 'can_buy': False}

    return render(request, 'product_detail.html', context)


def buy_product(request, id):
    product = Products.objects.get(id=id)
    user = Student.objects.get(id=request.user.id)

    if user.coins >= product.price and product.count > 0:
        user.coins -= product.price
        product.count = max(product.count - 1, 0)  # Ensure count does not go below 0
        product.save()
        user.save()
        Shop_history.objects.create(product=product, buyer=user)
        return redirect('shop')
    else:
        return redirect('detail_product', id=id)
