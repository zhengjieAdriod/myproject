from django.http import JsonResponse
# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from cases.models import SchemeInService, Worker, Service
from comments.models import Owner
from order.models import Order
import datetime


@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def add_order(request):
    param = request.data
    worker_pk = param['worker_pk']
    owner_telephone = param['owner_telephone']
    service_pk = param['service_pk']
    scheme_in_service_pk = param['schemeInService_pk']
    worker = Worker.objects.get(pk=worker_pk)
    service = Service.objects.get(pk=service_pk)
    scheme_in_service = SchemeInService.objects.get(pk=scheme_in_service_pk)
    owners = Owner.objects.filter(telephone=owner_telephone)
    if len(owners) > 0:
        owner = owners[0]
        pass
    else:
        # todo 自动成为新的用户
        owner = Owner(telephone=owner_telephone)
        owner.save()
        pass
    order = Order()
    order.worker = worker
    order.owner = owner
    import time
    now = datetime.datetime.now()
    tt = int(time.mktime(now.timetuple()))
    order.order_num = str(worker.pk) + str(owner_telephone) + str(tt)
    order.state = '已下单'
    order.service = service
    order.schemeInService = scheme_in_service
    order.save()
    return JsonResponse("hello", safe=False)



