from django.utils import timezone
from .models import Devices,Users,Device_history


# 期間１と期間２が被っている場合はTrue,被らない場合はFalse
def dates_Overlap(rental_start1,rental_limit1,rental_start2,rental_limit2):
    if rental_limit2 < rental_start1 or rental_limit1 < rental_start2:
        return False
    else:
        return True

def get_lend_column(column_number):
    columns = ["user_id__user_id","user_id__name","device_id__device_id","rental_start","rental_limit","registration_date"]
    return columns[column_number]

def get_devices_column(column_number):
    columns = ["device_id","maker","OS","memory","storage","CPU","GPU","inventory","broken_flag","registration_date"]
    return columns[column_number]

def get_users_column(column_number):
    columns = ["user_id","name","department","tel_number","mail_address","age","position"]
    return columns[column_number]

def classify_for_Devices(sort_rule=False,column_str="rental_start"):
    device_list_ = Devices.objects.filter(delete_flag=0)
    device_list_1 = []
    device_list_2 = []
    for i,v in enumerate(device_list_):
        data = Device_history.objects.filter(device_id=v.id,rental_end=None).order_by('rental_start').first()
        if not data == None:
            if column_str=="rental_start":
                device_list_1.append([data.rental_start,v.id])
            elif column_str=="rental_limit":
                device_list_1.append([data.rental_limit,v.id])
        else:
            device_list_2.append(v.id)
    device_list_1 = sorted(device_list_1,reverse=sort_rule)
    loop_first = True
    for i in device_list_1:
        if loop_first:
            queryset1 = Devices.objects.filter(pk=i[1])
            loop_first = False
        tmp = Devices.objects.filter(pk=i[1])
        queryset1 = queryset1 | tmp
    queryset2 = Devices.objects.filter(pk__in=device_list_2)
    return (queryset1,queryset2)

def classify_status_use(table_name):
    today = timezone.now()
    if table_name=="Devices":
        list_ = Devices.objects.filter(delete_flag=0)
    elif table_name=="Users":
        list_ = Users.objects.filter(delete_flag=0)
    elif table_name=="Device_history":
        list_ = Device_history.objects.filter(rental_end=None)
    list_1 = [] # 利用予定
    list_2 = [] # 利用中
    list_3 = [] # 利用中（期限超過）
    list_4 = [] # 空
    for i,v in enumerate(list_):
        if table_name=="Devices":
            data = Device_history.objects.filter(device_id=v.id,rental_end=None).order_by('rental_start').first()
        elif table_name=="Users":
            data = Device_history.objects.filter(user_id=v.id,rental_end=None).order_by('rental_start').first()
        elif table_name=="Device_history":
            data = v
        if not data == None:
            if data.rental_start >= today:
                # 利用予定
                list_1.append(v.id)
            elif data.rental_limit <= today:
                # 利用中（期限超過）
                list_3.append(v.id)
            else:
                # 利用中
                list_2.append(v.id)
        else:
            list_4.append(v.id)
    if table_name=="Devices":
        queryset1 = Devices.objects.filter(pk__in=list_1)
        queryset2 = Devices.objects.filter(pk__in=list_2)
        queryset3 = Devices.objects.filter(pk__in=list_3)
        queryset4 = Devices.objects.filter(pk__in=list_4)
    elif table_name=="Users":
        queryset1 = Users.objects.filter(pk__in=list_1)
        queryset2 = Users.objects.filter(pk__in=list_2)
        queryset3 = Users.objects.filter(pk__in=list_3)
        queryset4 = Users.objects.filter(pk__in=list_4)
    elif table_name=="Device_history":
        queryset1 = Device_history.objects.filter(pk__in=list_1)
        queryset2 = Device_history.objects.filter(pk__in=list_2)
        queryset3 = Device_history.objects.filter(pk__in=list_3)
        queryset4 = Device_history.objects.filter(pk__in=list_4)
    return (queryset1,queryset2,queryset3,queryset4)

def classify_gender_for_Users():
    user_list_ = Users.objects.filter(delete_flag=0)
    user_list_1 = []
    user_list_2 = []
    user_list_3 = []
    for i in user_list_:
        if i.gender=="　":
            user_list_1.append(i.id)
        elif i.gender=="男性":
            user_list_2.append(i.id)
        else:
            user_list_3.append(i.id)
    queryset1 = Users.objects.filter(pk__in=user_list_1)
    queryset2 = Users.objects.filter(pk__in=user_list_2)
    queryset3 = Users.objects.filter(pk__in=user_list_3)
    return (queryset1,queryset2,queryset3)