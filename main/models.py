from django.db import models
from django.contrib.auth.models import Group, User
from django.dispatch import receiver
from django.db.models.signals import post_save


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


# ユーザーモデルと1:1リレーションで同期して登録する
@receiver(post_save, sender=User)
def create_user_operator(sender, instance, created, **kwargs):
    if created:
        Operator.objects.create(user=instance)


# ユーザーモデルと1:1リレーションで同期して更新する
@receiver(post_save, sender=User)
def save_user_operator(sender, instance, **kwargs):
    instance.operator.save()


# 会場マスター
class Venue(models.Model):
    class Meta:
        verbose_name = '会場マスター'
        verbose_name_plural = '会場マスター'
        db_table = 'venue'

    name = models.CharField(verbose_name='会場名', default='', max_length=40, blank=False, null=False)
    capacity = models.IntegerField(verbose_name='収容人数', default=0, blank=False, null=False)
    hidden_flag = models.BooleanField(verbose_name='非表示フラグ', default=False, blank=True, null=True)

    def __str__(self):
        return 'Venue Master id:' + str(self.id) + ', Name：' + self.name + '(' + str(self.capacity) + ')'


# 接種者マスター
class Recipient(models.Model):
    class Meta:
        verbose_name = '接種者マスター'
        verbose_name_plural = '接種者マスター'
        db_table = 'recipient'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(verbose_name='年齢', default=0, blank=False, null=False)
    hidden_flag = models.BooleanField(verbose_name='非表示フラグ', default=False, blank=True, null=True)

    def __str__(self):
        return 'Recipient Master id:' + str(self.id) + ', Name：' + self.user.username
