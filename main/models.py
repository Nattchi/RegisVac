from django.db import models
from django.contrib.auth.models import Group, User
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid


class UserGroup(models.Model):
    class Meta:
        verbose_name = '認証グループテーブル'
        verbose_name_plural = '認証グループテーブル'
        db_table = 'user_group'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    def __str__(self):
        return 'username:' + self.user.username + ", group:" + self.group.name


# 作業者マスター
class Operator(models.Model):
    class Meta:
        verbose_name = '操作者マスター'
        verbose_name_plural = '操作者マスター'
        db_table = 'operator'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hidden_flag = models.BooleanField(verbose_name='非表示フラグ', default=False, blank=True, null=True)

    def __str__(self):
        return 'Operator Master id:' + str(self.id) + ', username：' + self.user.username + \
               ', Name：' + self.user.first_name + self.user.last_name


# 被接種者
class Recipient(models.Model):
    class Meta:
        verbose_name = '被接種者'
        verbose_name_plural = '被接種者'
        db_table = 'recipient'

    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for Recipient", verbose_name='接種番号')
    last_name = models.CharField(max_length=100, verbose_name='姓')
    first_name = models.CharField(max_length=100, verbose_name='名')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='生年月日')
    Phonenumber = models.IntegerField(max_length=200, verbose_name='電話番号')
    Email_address = models.EmailField(max_length=254, verbose_name='Email')
    Address = models.CharField(max_length=200, verbose_name='住所')
    Basic_illness = models.CharField(max_length=200, verbose_name='基礎疾患')
    VAC_STATUS = (
        ('a', '未接種'),
        ('b', '1回目接種完了'),
        ('c', '2回目接種完了'),
        ('d', '不接種'),
    )
    status = models.CharField(max_length=1, choices=VAC_STATUS, blank=True, default='a', verbose_name='接種状態')


    def __str__(self):
        return ' 接種番号:' + str(self.ID) + ', 名前：' + self.last_name + self.first_name


# ユーザーモデルと1:1リレーションで同期して登録する
@receiver(post_save, sender=User)
def create_user_operator(sender, instance, created, **kwargs):
    if created:
        Operator.objects.create(user=instance)


# ユーザーモデルと1:1リレーションで同期して更新する
@receiver(post_save, sender=User)
def save_user_operator(sender, instance, **kwargs):
    instance.operator.save()
