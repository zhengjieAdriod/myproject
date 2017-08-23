import json

from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from cases.models import Service, Worker
from cases.serializers import ServiceSerializer, WorkerSerializer, SchemeInServiceSerializer
from worker_manage.forms import ServiceForm


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
@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def update_edit_service(request, service_pk):
    form = ServiceForm(request.POST)
    comment = form.save(commit=False)
    comment.save()
    return None
