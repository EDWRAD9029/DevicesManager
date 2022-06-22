from django.utils import timezone
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView
from .models import Devices,Users,Device_history
from .forms import DevicesForm,UsersForm,DeviceHistoryAddForm,DeviceHistoryEditForm
from ._getState import classify_gender_for_Users
from ._getState import get_lend_column,get_devices_column,get_users_column
from ._getState import classify_status_use,classify_for_Devices



class MainView(TemplateView):
    template_name = 'main.html'



def lend(request):
    return lendSort(request,-1)



def lendSort(request,column_number):
    Sorts = {}
    if 0 <= column_number and column_number<100:
        column_str = get_lend_column(column_number//2)
        if column_number%2 ==0:
            lend_list = Device_history.objects.filter(rental_end=None).order_by(str('-'+column_str))
        else:
            lend_list = Device_history.objects.filter(rental_end=None).order_by(str(column_str))
        Sorts[str(column_str+str( (column_number % 2)+1 ))] = True
    elif 100<=column_number:
        if column_number//100 ==1:
            column_str = "status_use"
            (queryset1,queryset2,queryset3,_) = classify_status_use(table_name="Device_history")
            if column_number%100 == 1:
                lend_list = queryset1 | queryset2 | queryset3
            elif column_number%100 == 2:
                lend_list = queryset2 | queryset3 | queryset1
            elif column_number%100 == 3:
                lend_list = queryset3 | queryset1 | queryset2
        Sorts[str(column_str+str(column_number % 100))] = True
    else:
        lend_list = Device_history.objects.filter(rental_end=None)
    context = {'lend_list': lend_list,
               'today':timezone.now(),
               'Sorts': Sorts,
               'page_lend':True}
    return render(request, 'lend.html', context)



def lendDelete(request):
    status_use_list = request.POST.getlist("status_use")
    delete_list = [i.split('+')[1][:-1] for i in status_use_list if "返却済" in i]
    print(status_use_list)
    print(delete_list)
    Device_history.objects.filter(pk__in=delete_list,rental_end=None).update(rental_end=timezone.now())
    return redirect('polls:lend')



def devices(request):
    return devicesSort(request,-1)



def devicesSort(request,column_number):
    Sorts = {}
    if 0 <= column_number and column_number<100:
        column_str = get_devices_column(column_number//2)
        if column_number%2 ==0:
            device_list = Devices.objects.filter(delete_flag=0).order_by(str('-'+column_str))
        else:
            device_list = Devices.objects.filter(delete_flag=0).order_by(str(column_str))
        Sorts[str(column_str+str( (column_number % 2)+1 ))] = True
    elif 100<=column_number:
        if column_number//100 ==1:
            column_str = "status_use"
            (queryset1,queryset2,queryset3,queryset4) = classify_status_use(table_name="Devices")
            if column_number%100 == 1:
                device_list = queryset1 | queryset2 | queryset3 | queryset4
            elif column_number%100 == 2:
                device_list = queryset2 | queryset3 | queryset4 | queryset1
            elif column_number%100 == 3:
                device_list = queryset3 | queryset4 | queryset1 | queryset2
            elif column_number%100 == 4:
                device_list = queryset4 | queryset1 | queryset2 | queryset3
        elif column_number//100 ==2:
            column_str = "rental_start"
            (queryset1,queryset2) = classify_for_Devices(sort_rule=bool(column_number%100 == 1),column_str="rental_start")
            device_list = queryset1 | queryset2
        elif column_number//100 ==3:
            column_str = "rental_limit"
            (queryset1,queryset2) = classify_for_Devices(sort_rule=bool(column_number%100 == 1),column_str="rental_limit")
            device_list = queryset1 | queryset2
        Sorts[str(column_str+str(column_number % 100))] = True
    else:
        device_list = Devices.objects.all()
    addRentDateForDevices(device_list)
    context = {'device_list': device_list,
               'today':timezone.now(),
               'Sorts': Sorts,
               'page_devices':True}
    return render(request, 'devices.html', context)



def addRentDateForDevices(lists):
    for i,v in enumerate(lists):
        data = Device_history.objects.filter(device_id=v.id,rental_end=None).order_by('rental_start').first()
        if not data == None:
            tmp = lists[i].__dict__
            tmp["rental_start"] = data.rental_start
            tmp["rental_limit"] = data.rental_limit
            tmp["rental_end"] = data.rental_end



def devicesDelete(request):
    check = request.POST.getlist("delete")
    Devices.objects.filter(pk__in=check).update(delete_flag=1)
    return redirect('polls:devices')



def users(request):
    return usersSort(request,-1)



def usersSort(request,column_number):
    Sorts = {}
    if 0 <= column_number and column_number<100:
        column_str = get_users_column(column_number//2)
        if column_number%2 ==0:
            user_list = Users.objects.filter(delete_flag=0).order_by(str('-'+column_str))
        else:
            user_list = Users.objects.filter(delete_flag=0).order_by(str(column_str))
        Sorts[str(column_str+str( (column_number % 2)+1 ))] = True
    elif 100<=column_number:
        if column_number//100 ==1:
            column_str = "status_use"
            (queryset1,queryset2,queryset3,queryset4) = classify_status_use(table_name="Users")
            if column_number%100 == 1:
                user_list = queryset1 | queryset2 | queryset3 | queryset4
            elif column_number%100 == 2:
                user_list = queryset2 | queryset3 | queryset4 | queryset1
            elif column_number%100 == 3:
                user_list = queryset3 | queryset4 | queryset1 | queryset2
            elif column_number%100 == 4:
                user_list = queryset4 | queryset1 | queryset2 | queryset3
        elif column_number//100 ==2:
            column_str = "gender"
            (queryset1,queryset2,queryset3) = classify_gender_for_Users()
            if column_number%100 == 1:
                user_list = queryset2 | queryset3 | queryset1
            elif column_number%100 == 2:
                user_list = queryset3 | queryset2 | queryset1
            elif column_number%100 == 3:
                user_list = queryset1 | queryset2 | queryset3
        Sorts[str(column_str+str(column_number % 100))] = True
    else:
        user_list = Users.objects.all()
    addRentDateForUsers(user_list)
    context = {'user_list': user_list,
               'today':timezone.now(),
               'Sorts': Sorts,
               'page_users':True}
    return render(request, 'users.html', context)



def addRentDateForUsers(lists):
    for i,v in enumerate(lists):
        data = Device_history.objects.filter(user_id=v.id,rental_end=None).order_by('rental_start').first()
        if not data == None:
            tmp = lists[i].__dict__
            tmp["rental_start"] = data.rental_start
            tmp["rental_limit"] = data.rental_limit
            tmp["rental_end"] = data.rental_end



def usersDelete(request):
    check = request.POST.getlist("delete")
    Users.objects.filter(pk__in=check).update(delete_flag=1)
    return redirect('polls:users')



def lendAdd(request):
    params = {'title':'貸出情報入力',
              'button_name':'登録',
              'form': DeviceHistoryAddForm()}
    if request.method == 'POST':
        form = DeviceHistoryAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:lend')
        else:
            form = DeviceHistoryAddForm(request.POST)
            params["form"] = form
    return render(request, 'lendEdit.html', params)



def lendEdit(request,pk):
    lend = get_object_or_404(Device_history, pk=pk)
    params = {'lend':lend,
              'title':'貸出情報入力',
              'button_name':'変更',
              'form': None}
    if request.method == 'POST':
        form = DeviceHistoryEditForm(request.POST,instance=lend)
        if form.is_valid():
            form.save()
            return redirect('polls:lend')
        else:
            params["form"] = form
    else:
        lend_initial = {
            'user_id': lend.user_id,
            'device_id': lend.device_id,
            'rental_start': lend.rental_start,
            'rental_limit': lend.rental_limit}
        params['form'] = DeviceHistoryEditForm(initial=lend_initial)
    return render(request, 'lendEdit.html', params)



def devicesEdit(request,pk):
    if not pk==0:
        device = get_object_or_404(Devices, pk=pk)
        params = {'device_':device,
                  'title':'機器情報入力',
                  'button_name':'変更',
                  'form': None}
        if request.method == 'POST':
            form = DevicesForm(request.POST,instance=device)
            if form.is_valid():
                form.save()
                return redirect('polls:devices')
            else:
                form = DevicesForm(request.POST)
                params["form"] = form
        else:
            params['form'] = DevicesForm(initial=device.__dict__)
    else:
        params = {'title':'機器情報入力',
                  'button_name':'登録',
                  'form': DevicesForm()}
        if request.method == 'POST':
            form = DevicesForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('polls:devices')
            else:
                form = DevicesForm(request.POST)
                params["form"] = form
    return render(request, 'devicesEdit.html', params)
 


def usersEdit(request,pk):
    if not pk==0:
        user = get_object_or_404(Users, pk=pk)
        params = {'user_':user,
                  'title':'社員情報入力',
                  'button_name':'変更',
                  'form': None}
        if request.method == 'POST':
            form = UsersForm(request.POST,instance=user)
            if form.is_valid():
                form.save()
                return redirect('polls:users')
            else:
                form = UsersForm(request.POST)
                params["form"] = form
        else:
            params['form'] = UsersForm(initial=user.__dict__)
    else:
        params = {'title':'社員情報入力',
                  'button_name':'登録',
                  'form': UsersForm()}
        if request.method == 'POST':
            form = UsersForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('polls:users')
            else:
                form = UsersForm(request.POST)
                params["form"] = form
    return render(request, 'usersEdit.html', params)

    