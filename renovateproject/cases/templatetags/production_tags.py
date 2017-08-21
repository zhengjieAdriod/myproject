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


@register.simple_tag
def get_worker_post(pk):
    workers = Worker.objects.filter(pk=pk)
    if len(workers) > 0:
        worker = workers[0]
        return worker.post_set.all()
    return []


# 获得worker下的所有评论
@register.simple_tag
def get_worker_comment(pk):
    workers = Worker.objects.filter(pk=pk)
    if len(workers) > 0:
        worker = workers[0]
        return worker.comment_set.all()
    return []
