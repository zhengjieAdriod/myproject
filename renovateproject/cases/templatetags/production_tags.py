from django import template
from ..models import Worker

register = template.Library()


@register.simple_tag
def get_worker_production(pk):
    workers = Worker.objects.filter(pk=pk)
    if len(workers) > 0:
        worker = workers[0]
        return worker.service_set.all()
    return []
