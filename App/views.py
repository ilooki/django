import json

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from App import models


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        type = request.POST.get('type')
        response = {'msg': '', 'status': False}
        uid = request.POST.get('uid')
        pwd = request.POST.get('pwd')
        if type == 'login':
            if len(models.User.objects.filter(uid=uid, password=pwd)) != 0:
                response['status'] = True
                request.session['uid'] = uid
                return HttpResponse(json.dumps(response))
            else:
                response['msg'] = '账号或密码错误'
                return HttpResponse(json.dumps(response))
        elif type == 'register':
            models.User.objects.create(uid=uid, password=pwd)
            response['status'] = True
            request.session['uid'] = uid
            return HttpResponse(json.dumps(response))
        else:
            response['msg'] = '该用户已经被注册'
            return HttpResponse(json.dumps(response))


def register(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        pwd = request.POST.get('pwd')
        if len(models.User.objects.filter(uid=uid)) != 0:
            return render(request, 'login.html', {'message': '该用户已经注册'})
        else:
            user = {
                'uid': uid,
                'password': pwd,
            }
            models.User.objects.create(**user)
            return render(request, 'home.html')


def home(request):
    if request.method == 'GET':
        response = {}
        announcements = models.Announcement.objects.filter()
        a_list = []
        for a in announcements:
            dic = {'a_id': a.id, 'a_title': a.a_title, 'a_content': a.a_content}
            a_list.append(dic)

        n = 10 if len(a_list) < 10 else len(a_list)
        response['a_list'] = a_list[::-1][0:n - 1]

        recommends = models.Topic.objects.filter(recommend=True)
        r_list = []
        for t in recommends:
            dic = {'t_id': t.id, 't_title': t.t_title, 't_introduce': t.t_introduce, 't_photo': t.t_photo}
            r_list.append(dic)
        response['r_list'] = r_list

        response['uid'] = request.session['uid']
        kinds = models.Kind.objects.filter()
        response['kinds'] = kinds
        return render(request, 'home.html', response)


def edit_pwd(request):
    if request.method == 'GET':
        uid = request.session.get('uid')
        return render(request, 'edit-pwd.html', {'uid': uid})
    if request.method == 'POST':
        uid = request.session.get('uid')
        old = request.POST.get('old_pwd')
        new1 = request.POST.get('new_pwd1')
        new2 = request.POST.get('new_pwd2')

        if new1 == new2 and len(models.User.objects.filter(uid=uid, password=old)) != 0:
            models.User.objects.filter(uid=uid).update(password=new1)
            return redirect('/home')


# 发布帖子的实现
def publish(request):
    if request.method == 'GET':
        kinds = models.Kind.objects.filter()
        response = {
            'kinds': kinds

        }
        return render(request, 'publish.html', response)
    elif request.method == 'POST':
        uid = request.session.get('uid')
        t_title = request.POST.get('t_title')
        t_introduce = request.POST.get('t_introduce')
        t_content = request.POST.get('t_content')
        t_kind = request.POST.get('t_kind')
        print(t_introduce, t_content, t_kind, t_title)

        obj = models.Topic.objects.create(t_title=t_title, t_introduce=t_introduce,
                                          t_content=t_content, t_kind=t_kind, t_uid=uid)
        t_id = obj.id
        t_photo = request.FILES.get('t_photo', None)
        t_photo_path = 'statics/img/t_photo/' + str(t_id) + '_' + t_photo.name

        if t_photo:
            import os
            file = open(os.path.join(t_photo_path), 'wb')
            for line in t_photo.chunks():
                file.write(line)
            file.close()

        models.Topic.objects.filter(id=t_id).update(t_photo='/' + t_photo_path)
        return redirect('/single/' + str(t_id))


def single(request, tid):
    if request.method == 'GET':
        try:
            topic = models.Topic.objects.get(id=tid)
        except Exception as e:
            return redirect('/home')
        uid = request.session['uid']
        t_time = topic.create_time
        t_kind = topic.t_kind
        t_content = topic.t_content
        t_uid = topic.t_uid
        t_title = topic.t_title
        t_photo = topic.t_photo
        t_introduce = topic.t_introduce

        response = {
            'uid': uid,
            'tid': tid,
            't_uid': t_uid,
            't_time': t_time,
            't_kind': t_kind,
            't_content': t_content,
            't_title': t_title,
            't_photo': t_photo,
            't_introduce': t_introduce

        }
        # 留言内容的处理
        replys = models.Reply.objects.filter(r_tid=tid)
        reply_list = []
        for reply in replys:
            single_reply = {
                'r_uid': reply.r_uid,
                'r_time': reply.r_time,
                'r_content': reply.r_content,
                'r_photo': reply.r_photo,
                'r_id': reply.id,
            }
            reply_list.append(single_reply)
        response['reply_list'] = reply_list
        return render(request, 'single.html', response)
    elif request.method == 'POST':
        uid = request.session.get('uid')

        if not uid:
            return redirect('/login')
        r_content = request.POST.get('r_content')
        obj = models.Reply.objects.create(r_tid=tid, r_uid=uid, r_content=r_content)
        r_id = str(obj.id)
        r_photo = request.FILES.get('r_photo')
        r_photo_path = ''
        if r_photo:
            r_photo_path = 'statics/img/r_photo' + r_id + '_' + r_photo.name
            import os
            file = open(os.path.join(r_photo_path), 'wb')
            for line in r_photo.chunks():
                file.write(line)
            file.close()

        models.Reply.objects.filter(id=r_id).update(r_photo='/' + r_photo_path)
        return redirect('/single/' + str(tid))


def admin(request):
    if request.method == 'GET':
        return render(request, 'admin.html')
    elif request.method == 'POST':
        admin_uid = request.POST.get('admin_id')
        admin_pwd = request.POST.get('admin_pwd')

        response = {'msg': '', 'status': False}

        if admin_uid == "root" and admin_pwd == "root":
            response['status'] = True
            request.session['admin_uid'] = 'root'
            return HttpResponse(json.dumps(response))
        else:
            response['msg'] = '用户或密码错误'
            return HttpResponse(json.dumps(response))


def announcement(request):
    if not request.session.get('admin_uid'):
        return redirect('/my_admin')

    # 查询
    if request.method == 'GET':
        announcements = models.Announcement.objects.filter()
        response = {'announcements': announcements}
        return render(request, 'announcement.html', response)

    # 删除 添加公告
    elif request.method == 'POST':
        p_type = request.POST.get('type')
        response = {'msg': '', 'status': False}
        if p_type == 'delete':
            a_id = request.POST.get('a_id')
            models.Announcement.objects.filter(id=a_id).delete()
            response['status'] = True
        elif p_type == 'create':
            a_title = request.POST.get('a_title')
            a_content = request.POST.get('a_content')
            models.Announcement.objects.create(a_title=a_title, a_content=a_content)
        return HttpResponse(json.dumps(response))


def kind_manage(request):
    if not request.session.get('admin_uid'):
        return redirect('/my_admin')

    # 查询板块
    if request.method == 'GET':
        kinds = models.Kind.objects.filter()
        response = {'kinds': kinds}
        return render(request, 'kind-manage.html', response)

    # 板块管理
    elif request.method == 'POST':
        p_type = request.POST.get('type')
        response = {'msg': '', 'status': False}
        if p_type == 'delete':
            k_id = request.POST.get('k_id')
            models.Kind.objects.filter(id=k_id).delete()
            response['status'] = True
        elif p_type == 'create':
            k_name = request.POST.get('k_name')
            models.Kind.objects.create(k_name=k_name)
        return HttpResponse(json.dumps(response))


def single_an(request, aid):
    if request.method == 'GET':
        try:
            an = models.Announcement.objects.get(id=aid)
        except Exception as e:
            return redirect('/home')
        a_title = an.a_title
        a_content = an.a_content

        response = {
            'a_title': a_title,
            'a_content': a_content,
        }
        return render(request, 'single-an.html', response)


# 帖子管理
def topic_manage(request):
    if not request.session.get('admin_uid'):
        return redirect('/my_admin')

    if request.method == 'GET':
        topics = models.Topic.objects.filter()
        response = {'topics': topics}
        return render(request, 'admin-home.html', response)

    # 推荐帖子
    elif request.method == 'POST':
        p_type = request.POST.get('type')
        response = {'msg': '', 'status': False}
        if p_type == 'delete':
            t_id = request.POST.get('t_id')
            models.Topic.objects.filter(id=t_id).delete()
            response['status'] = True
            return HttpResponse(json.dumps(response))
        if p_type == 'tuijian':
            t_id = request.POST.get('t_id')
            models.Topic.objects.filter(id=t_id).update(recommend=True)
            response['status'] = True
            return HttpResponse(json.dumps(response))
        if p_type == 'qxtuijian':
            t_id = request.POST.get('t_id')
            models.Topic.objects.filter(id=t_id).update(recommend=False)
            response['status'] = True
            return HttpResponse(json.dumps(response))


# 所有帖子
def all_tie(request, kid, reply_limit, time_limit):
    uid = request.session.get('uid')
    if request.method == 'GET':
        kinds = models.Kind.objects.filter()
        if kid == '0' and reply_limit == '0' and time_limit == '0':
            # 默认时间排序把帖子传过去
            topics = models.Topic.objects.filter()
        else:

            topics = models.Topic.objects.filter()

            # 筛选分类
            if kid != '0':
                topics = models.Topic.objects.filter(t_kind=kid)

            # 筛选回复数量
            tmp = []
            for topic in topics:
                # 查看每个帖子的回复数量
                count = len(models.Reply.objects.filter(r_tid=topic.id))
                # print(count)
                print(reply_limit)
                if reply_limit == '0':
                    pass
                elif reply_limit == '1':  # 1是大于100
                    print('到1了')
                    if count < 100:
                        print('到了')
                        continue
                elif reply_limit == '2':  # 2是30-100
                    if count < 30 or count > 100:
                        continue
                elif reply_limit == '3':  # 3是小于30
                    if count > 30:
                        continue
                tmp.append(topic)
            topics = tmp
            print(topics)

            # 筛选发布时间
            tmp = []
            for topic in topics:
                if time_limit == '0':  # 0是全部时间
                    pass
                elif time_limit == '1':  # 1是1个月内
                    # 如果在限制之前，就筛掉
                    pass
                elif time_limit == '2':  # 2是3个月内
                    # 如果在限制之前，就筛掉
                    pass
                elif time_limit == '3':  # 3是6个月内
                    # 如果在限制之前，就筛掉
                    pass
                elif time_limit == '4':  # 4是1年内
                    # 如果在限制之前，就筛掉
                    pass
                tmp.append(topic)
            topics = tmp

        response = {
            'topics': topics,
            'kinds': kinds,
            'kid': kid,
            'time_limit': time_limit,
            'reply_limit': reply_limit,
            'uid': uid,
        }
        return render(request, 'all.html', response)
    elif request.method == 'POST':
        # 搜索接收一个字段，查询标题或者简介里有关键字的帖子
        keys = request.POST.get('keys')
        # 按关键字查询标题里含有关键字的
        topics = models.Topic.objects.filter(t_title__icontains=keys)

        kinds = models.Kind.objects.filter()
        return render(request, 'all.html', {'topics': topics, 'kinds': kinds, 'uid': uid})
