import datetime

from django.db import models
# from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError



# 機器情報テーブル
class Devices(models.Model):
    device_id = models.CharField(
        # 管理画面での表示名
        verbose_name="機器番号",
        max_length=30,
        unique=True)
    maker = models.CharField(
        # 管理画面での表示名
        verbose_name="メーカ名",
        max_length=30,
        blank=True,
        null=True)
    OS = models.CharField(
        # 管理画面での表示名
        verbose_name="OS",
        max_length=30,
        blank=True,
        null=True)
    memory = models.CharField(
        # 管理画面での表示名
        verbose_name="メモリ",
        max_length=30,
        blank=True,
        null=True)
    storage = models.CharField(
        # 管理画面での表示名
        verbose_name="容量",
        max_length=30,
        blank=True,
        null=True)
    CPU = models.CharField(
        # 管理画面での表示名
        verbose_name="CPU",
        max_length=30,
        blank=True,
        null=True)
    GPU = models.CharField(
        # 管理画面での表示名
        verbose_name="GPU",
        max_length=30,
        blank=True,
        null=True)
    inventory = models.CharField(
        # 管理画面での表示名
        verbose_name="保管場所",
        max_length=30)
    BROKEN_CHOICES = (
        ("なし","なし"),
        ("あり","あり"),
        )
    broken_flag = models.CharField(
        # 管理画面での表示名
        verbose_name="故障",
        # 初期値
        default="なし",
        max_length=30,
        choices=BROKEN_CHOICES)
    registration_date = models.DateTimeField(
        # 管理画面での表示名
        verbose_name="機器登録日",
        # 初期値
        default=timezone.now())
    remarks = models.TextField(
        # 管理画面での表示名
        verbose_name="備考",
        blank=True,
        null=True)
    delete_flag = models.IntegerField(
        # 管理画面での表示名
        verbose_name="削除フラグ",
        # 初期値
        default=0)
    update_date = models.DateTimeField(
        # モデルインスタンスの度に現在時刻で更新
        auto_now=True)
    def __str__(self):
        return self.device_id

# # 社員情報テーブル
class Users(models.Model):
    user_id = models.IntegerField(
        # 管理画面での表示名
        verbose_name="社員番号",
        max_length=10,
        unique=True)
    name = models.CharField(
        # 管理画面での表示名
        verbose_name="氏名",
        max_length=30)
    age = models.IntegerField(
        # 管理画面での表示名
        verbose_name="年齢",
        max_length=3,
        blank=True,
        null=True)
    GENDER_CHOICES = (
        ("　","無回答"),
        ("男性","男性"),
        ("女性","女性"),
        )
    gender = models.CharField(
        # 管理画面での表示名
        verbose_name="性別",
        max_length=10,
        default="　",
        choices=GENDER_CHOICES)
    tel_number = models.CharField(
        # 管理画面での表示名
        verbose_name="電話番号",
        max_length=20,
        blank=True,
        null=True,
        unique=True)
    mail_address = models.CharField(
        # 管理画面での表示名
        verbose_name="メールアドレス",
        max_length=63,
        blank=True,
        null=True,
        unique=True)
    position = models.CharField(
        # 管理画面での表示名
        verbose_name="役職",
        max_length=30,
        blank=True,
        null=True)
    department = models.CharField(
        # 管理画面での表示名
        verbose_name="所属部署",
        max_length=30,
        blank=True,
        null=True)
    delete_flag = models.IntegerField(
        # 管理画面での表示名
        verbose_name="削除フラグ",
        max_length=1,
        # 初期値
        default=0)
    registration_date = models.DateTimeField(
        # 管理画面での表示名
        verbose_name="登録日",
        # 初期値
        default=timezone.now())
    update_date = models.DateTimeField(
        # モデルインスタンスの度に現在時刻で更新
        auto_now=True)
    def __str__(self):
        return str(self.user_id)

# 貸出情報テーブル
class Device_history(models.Model):
    device_id = models.ForeignKey(
        Devices,
        on_delete=models.CASCADE,
        # 管理画面での表示名
        verbose_name="機器番号")
    user_id = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        # 管理画面での表示名
        verbose_name="社員番号")
    rental_start = models.DateTimeField(
        # 管理画面での表示名
        verbose_name="貸出日")
    rental_limit = models.DateTimeField(
        # 管理画面での表示名
        verbose_name="返却予定日")
    rental_end = models.DateTimeField(
        # 管理画面での表示名
        verbose_name="返却日",
        blank=True,
        null=True)
    delete_flag = models.IntegerField(
        # 管理画面での表示名
        verbose_name="削除フラグ",
        # 初期値
        default=0)
    registration_date = models.DateTimeField(
        # 管理画面での表示名
        verbose_name="申請日",
        # 初期値
        default=timezone.now())
    update_date = models.DateTimeField(
        # モデルインスタンスの度に現在時刻で更新
        auto_now=True)
    def __str__(self):
        return str(self.user_id.user_id) +"_"+ str(self.device_id.device_id)