from django.db import models


# Create your models here.
class User(models.Model):
    uid = models.CharField(verbose_name='电话/用户号', max_length=16, unique=True)
    password = models.CharField(verbose_name='密码', max_length=16)
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = 'user'


class Topic(models.Model):
    t_uid = models.CharField(verbose_name='帖子所属的用户id', max_length=16)
    t_kind = models.CharField(verbose_name='帖子类型', max_length=16)
    t_photo = models.CharField(verbose_name='帖子图片', max_length=128, null=True)
    create_time = models.DateField(verbose_name='创建时间', auto_now_add=True)
    t_content = models.CharField(verbose_name='帖子正文', max_length=255)
    t_title = models.CharField(verbose_name='帖子标题', max_length=64)
    t_introduce = models.CharField(verbose_name='帖子简介', max_length=255)
    recommend = models.BooleanField(verbose_name='是否推荐', default=False)


class Kind(models.Model):
    k_name = models.CharField(verbose_name='类别', max_length=16, unique=True)

    class Meta:
        db_table = 'kind'


class Announcement(models.Model):
    a_title = models.CharField(verbose_name='公告标题', max_length=16, unique=True)
    a_content = models.CharField(verbose_name='公告内容', max_length=255, null=True)

    class Meta:
        db_table = 'announcement'


# 留言
class Reply(models.Model):
    r_tid = models.CharField(verbose_name='帖子ID', max_length=16)
    r_uid = models.CharField(verbose_name='留言者', max_length=16)
    r_content = models.CharField(verbose_name='留言内容', max_length=255)
    r_photo = models.CharField(verbose_name='图片', max_length=128, null=True)
    r_time = models.DateField(verbose_name='留言时间', auto_now_add=True)

    class Meta:
        db_table = 'reply'
