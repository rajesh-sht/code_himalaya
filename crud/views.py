from django.shortcuts import redirect, render, HttpResponseRedirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def user_list(request):
    users = User.objects.all().order_by('id')
    paginator = Paginator(users, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    # page = request.GET.get('page', 1)
    # paginator = Paginator(users, 10)
    # page = request.GET.get('page')
    # try:
    #     users = paginator.page(page)
    # except PageNotAnInteger:
    #     users = paginator.page(1)
    # except EmptyPage:
    #     users = paginator.page(paginator.num_pages)
    return render(request, 'user_list.html', {'users': page_obj})


def create_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        User.objects.create(name=name, phone=phone, address=address)
        return HttpResponseRedirect('/')

    return render(request, 'create.html')


def update_user(request, pk):
    id = User.objects.get(pk=pk)
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        id.name = name
        id.phone = phone
        id.address = address
        id.save()
        return HttpResponseRedirect('/')
    else:
        return render(request, 'update.html', {'ids': id},)


def delete_user(request, pk):
    id = User.objects.get(pk=pk)
    id.delete()
    return HttpResponseRedirect('/')
