# coding=utf-8
import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from cases.models import Service, Worker, SchemeInService
from cases.serializers import ServiceSerializer, WorkerSerializer, SchemeInServiceSerializer
from worker_manage.forms import ServiceForm, AddForm, SchemeInServiceForm


# todo 展示管家下的服务列表页
def manager(request, worker_pk):
    context = {'worker_pk': worker_pk}
    return render(request, 'worker_manage/service_manage.html', context)


# 切换内容
@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def tab_manage(request):
    index = request.POST.get('index')
    worker_pk = request.POST.get('worker_pk')
    workers = Worker.objects.filter(pk=worker_pk)
    if len(workers) == 0:
        return render(request, 'worker_manage/tab_errer.html', context={'test': '访问失败'})
    if index == '0':
        worker = workers[0]
        services = worker.service_set.all()
        services = sorted(services, key=lambda service: service.pk, reverse=True)
        services_serializer = ServiceSerializer(services, many=True)
        return render(request, 'worker_manage/tab_service.html',
                      context={'worker': worker, 'services': services, 'worker_pk': worker.pk,
                               'service_list': json.dumps(services_serializer.data)})
    if index == '1':
        return render(request, 'worker_manage/tab_order.html', context={'test': 1})
    if index == '2':
        return render(request, 'worker_manage/tab_comment.html', context={'test': 2})
    return render(request, 'worker_manage/tab_errer.html', context={'test': '访问失败'})


# todo 增加service 并关联worker
def add_service(request, worker_pk):
    workers = Worker.objects.filter(pk=worker_pk)
    if len(workers) > 0:
        worker = workers[0]
        worker_pk = worker.pk
        if request.method == 'POST':
            form = ServiceForm(request.POST)

            if form.is_valid():
                service_form = form.save(commit=False)

                file_dic = request.FILES.dict()
                l = len(file_dic)
                if l > 0:
                    image = file_dic['image']
                    service_form.image = image
                # 将评论和被评论的文章关联起来。
                service_form.worker = worker
                service_form.save()
                # return redirect(worker)  # todo 第一种重定向方式
                # todo 第二种重定向方式
                return redirect(reverse('worker_manage:manager-url', kwargs={'worker_pk': worker_pk}))
            else:
                # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
                context = {'form': form}
                return render(request, 'worker_manage/add_service.html', context=context)
        # get请求时
        form = ServiceForm()
        context = {'worker_pk': worker.pk, 'form': form}
        return render(request, 'worker_manage/add_service.html', context=context)


def all_valid(list):
    for item in list:
        if not item.is_valid():
            return False
    return True


# 提交编辑后的服务内容
# @api_view(['POST'])
# @csrf_exempt
# @permission_classes((AllowAny,))
# todo 提交编辑后的按钮,效果是刷新本页面) 另外删除子项的按钮也走了这里
def update_edit_service(request, service_pk):
    service = get_object_or_404(Service, pk=service_pk)
    worker_pk = service.worker.pk
    scheme_in_service_set = service.schemeinservice_set

    scheme_in_service_list = scheme_in_service_set.all()
    if request.method == 'POST':
        # 我们利用这些数据构造了 CommentForm 的实例，这样 Django 的表单就生成了。
        # todo 有了第二个参数 instance = service , 便是对原来数据的更新,而不是添加新的数据
        # form = ServiceForm(request.POST)
        form = ServiceForm(request.POST, request.FILES, instance=service, prefix='form')
        list = []

        i = 0
        for scheme_in_service in scheme_in_service_list:
            i = i + 1
            item_form = SchemeInServiceForm(request.POST, request.FILES, instance=scheme_in_service,
                                            prefix='item_form' + str(i))
            list.append(item_form)

        item_form = SchemeInServiceForm(request.POST, request.FILES,
                                        prefix='item_form')
        list.append(item_form)

        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if form.is_valid() and all_valid(list):
            # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            service_form = form.save(commit=False)
            for item in list:
                item_scheme_form = item.save(commit=False)
                if item_scheme_form.name != '':
                    item_scheme_form.save()
                    service_form.schemeinservice_set.add(item_scheme_form)
            service_form.worker = service.worker
            service_form.save()
            # return redirect(worker)  # todo 第一种重定向方式
            # todo 第二种重定向方式
            scheme_in_service_set = service.schemeinservice_set

            scheme_in_service_list = scheme_in_service_set.all()
            # return redirect(reverse('worker_manage:manager-url', kwargs={'worker_pk': worker_pk}))
            # form_item = SchemeInServiceForm(prefix='item_form')
            # list.append(form_item)
            # context = {'worker_pk': worker_pk, 'service_pk': service_pk, 'form': form,
            #            'form_item_list': list}
            # return render(request, 'worker_manage/edit_service.html', context=context)
        else:
            context = {'service_pk': service_pk, 'service': service, 'form': form, 'next': json.dumps('bottom')}
            return render(request, 'worker_manage/edit_service.html', context=context)

    form_item_list = []

    j = 0
    for scheme_in_service in scheme_in_service_list:
        j = j + 1
        form_item = SchemeInServiceForm(initial={'pk': scheme_in_service.pk,
                                                 'name': scheme_in_service.name,
                                                 'price': scheme_in_service.price,
                                                 'describe': scheme_in_service.describe,
                                                 'image': scheme_in_service.image, 'Service': service},
                                        prefix='item_form' + str(j))
        form_item.pk = scheme_in_service.pk
        form_item_list.append(form_item)
    last_scheme = scheme_in_service_list.last()
    if last_scheme is not None:
        if last_scheme.name != '':
            item_form = SchemeInServiceForm(prefix='item_form')
            form_item_list.append(item_form)
    if last_scheme is None:
        item_form = SchemeInServiceForm(prefix='item_form')
        form_item_list.append(item_form)
    form = ServiceForm(initial={'pk': service.pk, 'name': service.name,
                                'scope': service.scope,
                                'price': service.price,
                                'type': service.type,
                                'describe': service.describe,
                                'worker': service.worker,
                                'image': service.image}, prefix='form')
    context = {'worker_pk': worker_pk, 'service_pk': service_pk, 'form': form,
               'form_item_list': form_item_list, 'next': json.dumps('bottom')}
    return render(request, 'worker_manage/edit_service.html', context=context)


# todo 点击条目的编辑按钮展示服务数据包括服务的子项数据(同时也是,在编辑页面点击完成按钮(保存了编辑数据并跳转到前一页)
def update_edit_service_finish(request, service_pk):
    service = get_object_or_404(Service, pk=service_pk)
    worker_pk = service.worker.pk
    scheme_in_service_set = service.schemeinservice_set

    scheme_in_service_list = scheme_in_service_set.all()
    if request.method == 'POST':
        # 我们利用这些数据构造了 CommentForm 的实例，这样 Django 的表单就生成了。
        # todo 有了第二个参数 instance = service , 便是对原来数据的更新,而不是添加新的数据
        # form = ServiceForm(request.POST)
        form = ServiceForm(request.POST, request.FILES, instance=service, prefix='form')
        list = []

        i = 0
        for scheme_in_service in scheme_in_service_list:
            i = i + 1
            item_form = SchemeInServiceForm(request.POST, request.FILES, instance=scheme_in_service,
                                            prefix='item_form' + str(i))
            list.append(item_form)

        item_form = SchemeInServiceForm(request.POST, request.FILES,
                                        prefix='item_form')
        list.append(item_form)

        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if form.is_valid() and all_valid(list):
            # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            service_form = form.save(commit=False)
            for item in list:
                item_scheme_form = item.save(commit=False)
                if item_scheme_form.name != '':
                    item_scheme_form.save()
                    service_form.schemeinservice_set.add(item_scheme_form)
            service_form.worker = service.worker
            service_form.save()
            # return redirect(worker)  # todo 第一种重定向方式
            # todo 第二种重定向方式
            # scheme_in_service_set = service.schemeinservice_set
            #
            # scheme_in_service_list = scheme_in_service_set.all()
            return redirect(reverse('worker_manage:manager-url', kwargs={'worker_pk': worker_pk}))
            # form_item = SchemeInServiceForm(prefix='item_form')
            # list.append(form_item)
            # context = {'worker_pk': worker_pk, 'service_pk': service_pk, 'form': form,
            #            'form_item_list': list}
            # return render(request, 'worker_manage/edit_service.html', context=context)
        else:
            context = {'service_pk': service_pk, 'service': service, 'form': form, 'next': json.dumps('')}
            return render(request, 'worker_manage/edit_service.html', context=context)

    form_item_list = []

    j = 0
    for scheme_in_service in scheme_in_service_list:
        j = j + 1
        form_item = SchemeInServiceForm(initial={'pk': scheme_in_service.pk,
                                                 'name': scheme_in_service.name,
                                                 'price': scheme_in_service.price,
                                                 'describe': scheme_in_service.describe,
                                                 'image': scheme_in_service.image, 'Service': service},
                                        prefix='item_form' + str(j))
        form_item.pk = scheme_in_service.pk
        form_item_list.append(form_item)
    last_scheme = scheme_in_service_list.last()
    if last_scheme is not None:
        if last_scheme.name != '':
            item_form = SchemeInServiceForm(prefix='item_form')
            form_item_list.append(item_form)
    if last_scheme is None:
        item_form = SchemeInServiceForm(prefix='item_form')
        form_item_list.append(item_form)
    form = ServiceForm(initial={'pk': service.pk, 'name': service.name,
                                'scope': service.scope,
                                'price': service.price,
                                'type': service.type,
                                'describe': service.describe,
                                'worker': service.worker,
                                'image': service.image}, prefix='form')
    context = {'worker_pk': worker_pk, 'service_pk': service_pk, 'form': form,
               'form_item_list': form_item_list, 'next': json.dumps('')}
    return render(request, 'worker_manage/edit_service.html', context=context)


def index(request):
    if request.method == 'POST':  # 当提交表单时

        form = AddForm(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(str(int(a) + int(b)))

    else:  # 当正常访问时
        form = AddForm()
    return render(request, 'worker_manage/index.html', {'form': form})


# todo 删除子项的按钮(视图函数调用另一个视图函数)
def delete_item_service(request, service_pk, item_pk):
    scheme_list = SchemeInService.objects.filter(pk=item_pk)
    if scheme_list.count() > 0:
        scheme_list.first().delete()
    return update_edit_service(request, service_pk)


# todo 删除服务本项的按钮
@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def delete_service(request):
    param = request.data
    worker_pk = param['worker_pk']
    service_pk = param['service_pk']
    service_list = Service.objects.filter(pk=service_pk)
    if service_list.count() > 0:
        service = service_list.first()
        scheme_in_service_set = service.schemeinservice_set
        scheme_in_service_list = scheme_in_service_set.all()
        for scheme in scheme_in_service_list:
            scheme.delete()
        service.delete()
    return manager(request, worker_pk=worker_pk)
