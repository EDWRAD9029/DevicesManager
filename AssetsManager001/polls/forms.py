from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Devices,Users,Device_history
from ._getState import dates_Overlap

class DevicesForm(forms.ModelForm):
    class Meta:
        model = Devices
        fields = (
            'device_id',
            'maker',
            'OS',
            'memory',
            'storage',
            'CPU',
            'GPU',
            'inventory',
            'broken_flag',
            'remarks')
        labels = {
            'device_id': '機器番号',
            'maker': 'メーカ',
            'OS': 'OS',
            'memory': 'メモリ',
            'storage': '容量',
            'CPU': 'CPU',
            'GPU': 'GPU',
            'inventory': '保存場所',
            'broken_flag': '故障',
            'remarks': '備考'}
        help_texts = {
            'name': '',
            'maker': '',
            'OS': '',
            'memory': '',
            'storage': '',
            'CPU': '',
            'GPU': '',
            'inventory': '',
            'broken_flag': '',
            'remarks': ''}
        validators = {
            }


class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = (
            'user_id',
            'name',
            'age',
            'department',
            'tel_number',
            'mail_address',
            'gender',
            'position')
        labels = {
            'user_id': '社員番号',
            'name': '氏名',
            'age': '年齢',
            'department': '所属部署',
            'tel_number': '電話番号',
            'mail_address': 'メール',
            'gender': '性別',
            'position': '役職'}
        help_texts = {
            'user_id': '',
            'name': '',
            'age': '',
            'department': '',
            'tel_number': '',
            'mail_address': '',
            'gender': '',
            'position': ''}
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if not age == None:
            if age < 15 or age > 100:
                raise ValidationError('15〜100歳のみです！')
        return age


class DeviceHistoryAddForm(forms.ModelForm):
    class Meta:
        model = Device_history
        fields = (
            'user_id',
            'device_id',
            'rental_start',
            'rental_limit')
        labels = {
            'user_id': '社員番号',
            'device_id': '機器番号',
            'rental_start': '貸出日',
            'rental_limit': '返却予定日'}
        help_texts = {
            'user_id': '',
            'device_id': '',
            'rental_start': '',
            'rental_limit': ''}
    def __init__(self,*args,**kwargs):
        super(DeviceHistoryAddForm, self).__init__(*args, **kwargs)
        # 削除された機器・社員は選択できなくする
        self.fields['user_id'].queryset = Users.objects.filter(delete_flag=0)
        self.fields['device_id'].queryset = Devices.objects.filter(delete_flag=0,broken_flag="なし")
        self.fields['rental_start'].widget = forms.DateTimeInput(
            format = '%Y-%m-%dT%H:%M:%S', attrs = {'type': 'datetime-local', 'class': 'form-control'})
        self.fields['rental_limit'].widget = forms.DateTimeInput(
            format = '%Y-%m-%dT%H:%M:%S', attrs = {'type': 'datetime-local', 'class': 'form-control'})
    
    def clean_rental_start(self):
        return _valid_DeviceHistory_rental_start(self)
    def clean_rental_limit(self):
        return _valid_DeviceHistoryAdd_rental_limit(self)


class DeviceHistoryEditForm(forms.ModelForm):
    class Meta:
        model = Device_history
        fields = (
            'user_id',
            'device_id',
            'rental_start',
            'rental_limit')
        labels = {
            'user_id': '社員番号',
            'device_id': '機器番号',
            'rental_start': '貸出日',
            'rental_limit': '返却予定日'}
        help_texts = {
            'user_id': '',
            'device_id': '',
            'rental_start': '',
            'rental_limit': ''}
    def __init__(self,*args,**kwargs):
        super(DeviceHistoryEditForm, self).__init__(*args, **kwargs)
        # 削除された機器・社員は選択できなくする
        self.fields['user_id'].queryset = Users.objects.filter(delete_flag=0)
        self.fields['device_id'].queryset = Devices.objects.filter(delete_flag=0,broken_flag="なし")
        self.fields['rental_start'].widget = forms.DateTimeInput(
            format = '%Y-%m-%dT%H:%M:%S', attrs = {'type': 'datetime-local', 'class': 'form-control'})
        self.fields['rental_limit'].widget = forms.DateTimeInput(
            format = '%Y-%m-%dT%H:%M:%S', attrs = {'type': 'datetime-local', 'class': 'form-control'})
        # 利用状況に応じて編集不可にする
        user_id_initial = self.initial["user_id"]
        device_id_initial = self.initial["device_id"]
        rental_start_initial = self.initial["rental_start"]
        rental_limit_initial = self.initial["rental_limit"]
        today = timezone.now()
        if rental_start_initial >= today:
            # 利用予定の場合
            print("利用予定")
        elif rental_limit_initial <= today:
            # 利用中（期限超過）の場合
            print("利用中（期限超過）")
            if not type(user_id_initial) == int:
                self.fields['user_id'].queryset = Users.objects.filter(user_id=user_id_initial.user_id)
                self.fields['device_id'].queryset = Devices.objects.filter(device_id=device_id_initial.device_id)
            self.fields['rental_start'].widget.attrs['readonly'] = 'readonly'
        else:
            # 利用中の場合
            print("利用中")
            if not type(user_id_initial) == int:
                self.fields['user_id'].queryset = Users.objects.filter(user_id=user_id_initial.user_id)
                self.fields['device_id'].queryset = Devices.objects.filter(device_id=device_id_initial.device_id)
            self.fields['rental_start'].widget.attrs['readonly'] = 'readonly'
    
    def clean_rental_start(self):
        rental_start_initial = self.initial["rental_start"]
        rental_start = self.cleaned_data.get('rental_start')
        # 変更されたか
        if not rental_start_initial == rental_start:
            _ = _valid_DeviceHistory_rental_start(self)
        return rental_start
    def clean_rental_limit(self):
        return _valid_DeviceHistoryEdit_rental_limit(self)

def _valid_DeviceHistory_rental_start(self):
    rental_start = self.cleaned_data.get('rental_start')
    # 現在時刻以降か
    today = timezone.now()
    if rental_start < today:
        raise ValidationError('現在時刻以降でのみ貸出できます！')
    return rental_start

def _valid_DeviceHistoryAdd_rental_limit(self):
    rental_start = self.cleaned_data.get('rental_start')
    rental_limit = self.cleaned_data.get('rental_limit')
    device_id = self.cleaned_data.get('device_id')
    if rental_start == rental_limit:
        raise ValidationError('貸出期間がありません！')
    if rental_start > rental_limit:
        raise ValidationError('返却予定日を正しく入力してください！')
    # 貸出期間が被っていないか確認
    list_ = Device_history.objects.filter(device_id__device_id=device_id,rental_end=None)
    for i in list_:
        if dates_Overlap(i.rental_start,i.rental_limit,rental_start,rental_limit):
            self.add_error(None, '既に予約された期間と被っています！')
    return rental_limit

def _valid_DeviceHistoryEdit_rental_limit(self):
    rental_start = self.cleaned_data.get('rental_start')
    rental_limit = self.cleaned_data.get('rental_limit')
    device_id = self.cleaned_data.get('device_id')
    if rental_start == rental_limit:
        raise ValidationError('貸出期間がありません！')
    if rental_start > rental_limit:
        raise ValidationError('返却予定日を正しく入力してください！')
    # 貸出期間が被っていないか確認
    rental_start_initial = self.initial["rental_start"]
    rental_limit_initial = self.initial["rental_limit"]
    device_id_initial = self.initial["device_id"]
    list_ = Device_history.objects.filter(device_id__device_id=device_id_initial,rental_end=None)
    list_1 = [] # 選択されたレコードのpk
    for i in list_:
        if i.rental_start == rental_start_initial and i.rental_limit == rental_limit_initial:
            list_1.append(i.id)
    list_ = Device_history.objects.filter(device_id__device_id=device_id,rental_end=None)
    list_2 = []
    for i in list_:
        if not i.id in list_1:
            list_2.append(i.id)
    list_ = Device_history.objects.filter(pk__in=list_2)
    for i in list_:
        if dates_Overlap(i.rental_start,i.rental_limit,rental_start,rental_limit):
            self.add_error(None, '既に予約された期間と被っています！')
    return rental_limit