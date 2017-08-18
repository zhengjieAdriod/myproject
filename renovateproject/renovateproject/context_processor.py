from django.conf import settings as original_settings


def base_pic_url(request):
    return {'base_pic_url': 'http://' + request.META['REMOTE_ADDR'] + ':8000/media/'}


def ip_address(request):
    return {'ip_address': request.META['REMOTE_ADDR']}
