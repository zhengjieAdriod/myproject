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
        return render(request, 'worker_manage/tab_service.html',
                      context={'worker': worker, 'services': services})
    if index == '1':
        return render(request, 'worker_manage/tab_order.html', context={'test': 1})
    if index == '2':
        return render(request, 'worker_manage/tab_comment.html', context={'test': 2})
    return render(request, 'worker_manage/tab_errer.html', context={'test': '访问失败'})


# 增加service 并关联worker
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


# 增加service 并关联worker
# def add_service(request, worker_pk):
#     workers = Worker.objects.filter(pk=worker_pk)
#     if len(workers) > 0:
#         worker = workers[0]
#         worker_pk = worker.pk
#         if request.method == 'POST':
#             form = ServiceForm(request.POST)
#             if form.is_valid():
#                 service_form = form.save(commit=False)
#
#                 file_dic = request.FILES.dict()
#                 l = len(file_dic)
#                 if l > 0:
#                     image = file_dic['image']
#                     service_form.image = image
#                 # 将评论和被评论的文章关联起来。
#                 service_form.worker = worker
#                 service_form.save()
#                 # return redirect(worker)  # todo 第一种重定向方式
#                 # todo 第二种重定向方式
#                 # return redirect(reverse('worker_manage:manager-url', kwargs={'worker_pk': worker_pk}))
#                 form_item_list = []
#                 form_item = SchemeInServiceForm()
#                 form_item_list.append(form_item)
#                 form_item_list.append(form_item)
#                 context = {'service_pk': service_form.pk, 'worker_pk': worker.pk, 'form': form,
#                            'form_item_list': form_item_list}
#                 return render(request, 'worker_manage/add_service.html', context=context)
#             else:
#                 # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
#                 context = {'form': form}
#                 return render(request, 'worker_manage/add_service.html', context=context)
#         # get请求时
#         form = ServiceForm()
#         form_item_list = []
#         form_item = SchemeInServiceForm()
#         form_item_list.append(form_item)
#         form_item_list.append(form_item)
#         # -1来区别按钮是否可以点击
#         context = {'service_pk': -1, 'worker_pk': worker.pk, 'form': form, 'form_item_list': form_item_list}
#         return render(request, 'worker_manage/add_service.html', context=context)


# 增加service的子项 并关联worker，主service
def post_service_item(request, worker_pk, service_pk, form_item_pk):
    workers = Worker.objects.filter(pk=worker_pk)
    if len(workers) > 0:
        worker = workers[0]
        worker_pk = worker.pk
        scheme_in_services = SchemeInService.objects.filter(pk=form_item_pk)

        if request.method == 'POST':
            if len(scheme_in_services) > 0:
                scheme_in_service = scheme_in_services[0]
                form = SchemeInServiceForm(request.POST, instance=scheme_in_service)
            else:
                form = SchemeInServiceForm(request.POST)
            if form.is_valid():
                scheme_in_service_form = form.save(commit=False)

                file_dic = request.FILES.dict()
                l = len(file_dic)
                if l > 0:
                    image = file_dic['image']
                    scheme_in_service_form.image = image
                    # 将评论和被评论的文章关联起来。
                service = Service.objects.get(pk=service_pk)
                scheme_in_service_form.service = service
                scheme_in_service_form.save()
                service.schemeinservice_set.add(scheme_in_service_form)
                # return redirect(worker)  # todo 第一种重定向方式
                # todo 第二种重定向方式
                return redirect(reverse('worker_manage:manager-url', kwargs={'worker_pk': worker_pk}))
            else:
                # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
                context = {'form': form}
                return render(request, 'worker_manage/edit_service.html', context=context)


# 提交编辑后的服务内容
# @api_view(['POST'])
# @csrf_exempt
# @permission_classes((AllowAny,))
def update_edit_service(request, service_pk):
    service = get_object_or_404(Service, pk=service_pk)
    worker_pk = service.worker.pk
    if request.method == 'POST':
        # 我们利用这些数据构造了 CommentForm 的实例，这样 Django 的表单就生成了。
        # todo 有了第二个参数 instance = service , 便是对原来数据的更新,而不是添加新的数据
        # form = ServiceForm(request.POST)
        form = ServiceForm(request.POST, instance=service)
        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if form.is_valid():
            # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            service_form = form.save(commit=False)
            file_dic = request.FILES.dict()
            l = len(file_dic)
            if l > 0:
                image = file_dic['image']
                service_form.image = image
            # 将评论和被评论的文章关联起来。
            # comment.post = post
            # 最终将评论数据保存进数据库，调用模型实例的 save 方法
            service_form.worker = service.worker
            service_form.save()
            # return redirect(worker)  # todo 第一种重定向方式
            # todo 第二种重定向方式
            return redirect(reverse('worker_manage:manager-url', kwargs={'worker_pk': worker_pk}))
        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 因此我们传了三个模板变量给 detail.html，
            # 一个是文章（Post），一个是评论列表，一个是表单 form
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            # 具体请看下面的讲解。
            context = {'service_pk': service_pk, 'service': service, 'form': form}
            return render(request, 'worker_manage/edit_service.html', context=context)
            # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
            # return render(request, 'worker_manage/edit_service.html', context=context)
    # service_serializer = ServiceSerializer(service, many=False)
    # 'service': json.dumps(service_serializer.data),
    # form的初始化
    scheme_in_service_set = service.schemeinservice_set
    scheme_in_service_list = scheme_in_service_set.all()
    form_item_list = []
    for scheme_in_service in scheme_in_service_list:
        form_item = SchemeInServiceForm(initial={'pk': scheme_in_service.pk,
                                                 'name': scheme_in_service.name,
                                                 'price': scheme_in_service.price,
                                                 'describe': scheme_in_service.describe,
                                                 'image': scheme_in_service.image})
        form_item.pk = scheme_in_service.pk
        form_item_list.append(form_item)
    if len(scheme_in_service_list) < 1:
        form_item = SchemeInServiceForm()
        form_item.pk = 0
        form_item_list.append(form_item)
    form = ServiceForm(initial={'pk': service.pk, 'name': service.name,
                                'scope': service.scope,
                                'price': service.price,
                                'type': service.type,
                                'describe': service.describe,
                                'worker': service.worker,
                                'image': service.image})
    context = {'worker_pk': worker_pk, 'service_pk': service_pk, 'form': form,
               'form_item_list': form_item_list}
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
