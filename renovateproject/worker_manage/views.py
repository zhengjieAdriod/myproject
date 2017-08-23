import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from cases.models import Service, Worker
from cases.serializers import ServiceSerializer, WorkerSerializer, SchemeInServiceSerializer
from worker_manage.forms import ServiceForm, AddForm


def manager(request):
    return render(request, 'worker_manage/service_manage.html')


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
        return render(request, 'worker_manage/tab_service.html',
                      context={'test': 0, 'services': services})
    if index == '1':
        return render(request, 'worker_manage/tab_order.html', context={'test': 1})
    if index == '2':
        return render(request, 'worker_manage/tab_comment.html', context={'test': 2})
    return render(request, 'worker_manage/tab_errer.html', context={'test': '访问失败'})


# 展示将要编辑服务的内容
def edit_service(request, service_pk):
    services = Service.objects.filter(pk=service_pk)
    if len(services) > 0:
        service = services[0]
        worker = service.worker
        serializer = WorkerSerializer(worker, many=False)  # todo 实现返回单独的对象
        scheme_in_services = service.schemeinservice_set.all()
        scheme_in_services_serializer = SchemeInServiceSerializer(scheme_in_services, many=True)
        return render(request, 'worker_manage/edit_service.html',
                      context={'worker': serializer.data, 'service_pk': service_pk, 'service': service,
                               'scheme_in_services': scheme_in_services,
                               'scheme_in_services_js': json.dumps(scheme_in_services_serializer.data)})


# 提交编辑后的服务内容
# @api_view(['POST'])
# @csrf_exempt
# @permission_classes((AllowAny,))
def update_edit_service(request, service_pk):
    service = get_object_or_404(Service, pk=service_pk)
    if request.method == 'POST':
        # 用户提交的数据存在 request.POST 中，这是一个类字典对象。
        # 我们利用这些数据构造了 CommentForm 的实例，这样 Django 的表单就生成了。
        form = ServiceForm(request.POST)

        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if form.is_valid():
            # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment = form.save(commit=False)

            # 将评论和被评论的文章关联起来。
            # comment.post = post

            # 最终将评论数据保存进数据库，调用模型实例的 save 方法
            comment.save()

            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return render(request, 'worker_manage/edit_service.html',
                          context={'service_pk': service_pk, 'service': service})

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
    form = ServiceForm()
    context = {'service_pk': service_pk, 'service': service, 'form': form}
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
