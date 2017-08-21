from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from cases.models import Post, Worker, Service


# 获得案例列表(包含根据worker获得案例列表)
def cases(request, worker_pk=0):
    # return HttpResponse("欢迎访问首页！")东城西城海淀朝阳丰台房山通州顺义昌平大兴怀柔门头沟石景山
    state_list = ['全部', '已完工', '未完工']
    district_list = ['全部', '东城', '西城', '海淀', '朝阳', '丰台', '通州']
    post_list = Post.objects.all()
    if worker_pk is not None and int(worker_pk) > 0:
        worker_db = Worker.objects.get(pk=worker_pk)
        post_list = Post.objects.filter(worker=worker_db)
    return render(request, 'cases/index.html',
                  context={'post_list': post_list, 'stateList': state_list, 'districtList': district_list,
                           })


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'cases/detail.html', context={'post': post})


def service_and_post_of_worker(request, worker_pk):
    return render(request, 'cases/worker_show.html', context={'worker_pk': worker_pk})


def service_detail(request, service_pk):
    services = Service.objects.filter(pk=service_pk)
    if len(services) > 0:
        service = services[0]
        scheme_in_services = service.schemeinservice_set.all()
        return render(request, 'cases/service_detail.html',
                      context={'service_pk': service_pk, 'service': service, 'scheme_in_services': scheme_in_services})


@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def add_order(request):
    a = range(100)
    return JsonResponse("hello", safe=False)
