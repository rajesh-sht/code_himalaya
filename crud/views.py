from django.shortcuts import redirect, render, HttpResponseRedirect
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.


def user_list(request):
    users = User.objects.all().order_by('id')
    paginator = Paginator(users, 8)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request, 'user_list.html', {'users': page_obj})


def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            # if phone == "":
            #     messages.error(request, "Must be Filled!")
            #     return HttpResponseRedirect('/create-user/')
            if phone.isdigit() == False:
                messages.error(request, "Must be integer!")
                return HttpResponseRedirect('/create-user/')
            if len(phone) > 10:
                messages.error(request, "Must be of 10digits!")
                return HttpResponseRedirect('/create-user/')

            User.objects.create(name=name, phone=phone, address=address)
            messages.success(request, 'User added successfully!')
            return HttpResponseRedirect('/')
    else:
        form = UserForm()

    return render(request, 'create.html', {"form": form})


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
        messages.success(request, 'User update successfully!')

        return HttpResponseRedirect('/')
    else:
        return render(request, 'update.html', {'ids': id},)


def delete_user(request, pk):
    id = User.objects.get(pk=pk)
    id.delete()
    return HttpResponseRedirect('/')


def search(request):
    if request.method == 'GET':
        name = request.GET.get('search', None)
        if name:
            check = User.objects.filter(name__icontains=name)
            check1 = User.objects.filter(address__icontains=name)
            return render(request, "search.html", {"users": check, "users1": check1})
    else:
        return redirect('/')
