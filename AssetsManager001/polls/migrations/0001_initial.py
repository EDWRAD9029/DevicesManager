# Generated by Django 4.0.4 on 2022-06-13 05:32

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=30, verbose_name='機器番号')),
                ('maker', models.CharField(blank=True, max_length=30, null=True, verbose_name='メーカ名')),
                ('OS', models.CharField(blank=True, max_length=30, null=True, verbose_name='OS')),
                ('memory', models.CharField(blank=True, max_length=30, null=True, verbose_name='メモリ')),
                ('storage', models.CharField(blank=True, max_length=30, null=True, verbose_name='容量')),
                ('CPU', models.CharField(blank=True, max_length=30, null=True, verbose_name='CPU')),
                ('GPU', models.CharField(blank=True, max_length=30, null=True, verbose_name='GPU')),
                ('inventory', models.CharField(max_length=30, verbose_name='保管場所')),
                ('broken_flag', models.CharField(choices=[('なし', 'なし'), ('あり', 'あり')], default='なし', max_length=30, verbose_name='故障')),
                ('registration_date', models.DateTimeField(default=datetime.datetime(2022, 6, 13, 5, 32, 47, 61835, tzinfo=utc), verbose_name='機器登録日')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='備考')),
                ('delete_flag', models.IntegerField(default=0, verbose_name='削除フラグ')),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(max_length=10, verbose_name='社員番号')),
                ('name', models.CharField(max_length=30, verbose_name='氏名')),
                ('age', models.IntegerField(blank=True, max_length=3, null=True, verbose_name='年齢')),
                ('gender', models.CharField(choices=[('\u3000', '無回答'), ('男性', '男性'), ('女性', '女性')], default='\u3000', max_length=10, verbose_name='性別')),
                ('tel_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='電話番号')),
                ('mail_address', models.CharField(blank=True, max_length=63, null=True, verbose_name='メールアドレス')),
                ('position', models.CharField(blank=True, max_length=30, null=True, verbose_name='役職')),
                ('department', models.CharField(blank=True, max_length=30, null=True, verbose_name='所属部署')),
                ('delete_flag', models.IntegerField(default=0, max_length=1, verbose_name='削除フラグ')),
                ('registration_date', models.DateTimeField(default=datetime.datetime(2022, 6, 13, 5, 32, 47, 99735, tzinfo=utc), verbose_name='登録日')),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Device_history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rental_start', models.DateTimeField(verbose_name='貸出日')),
                ('rental_limit', models.DateTimeField(verbose_name='返却予定日')),
                ('rental_end', models.DateTimeField(blank=True, null=True, verbose_name='返却日')),
                ('delete_flag', models.IntegerField(default=0, verbose_name='削除フラグ')),
                ('registration_date', models.DateTimeField(default=datetime.datetime(2022, 6, 13, 5, 32, 47, 99735, tzinfo=utc), verbose_name='申請日')),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.devices', verbose_name='機器番号')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.users', verbose_name='社員番号')),
            ],
        ),
    ]