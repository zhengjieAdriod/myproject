from django.forms import forms
from django.shortcuts import render
from rest_framework import viewsets
from cases.serializers import PostSerializer, StartInImageSerializer, ProtectionImageSerializer, \
    WorkSiteImageSerializer, FinishImageSerializer, WorkerSerializer
from .models import Post, StartInImage, ProtectionImage, WorkSiteImage, FinishImage, Worker, Service
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes, detail_route
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
import json
from django.utils import timezone


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    # v = self.kwargs.get('village')
    # queryset = Post.objects.filter(village="云景里")
    serializer_class = PostSerializer


def get_district_name(district):
    if district == '1':
        return "北京-朝阳"
    if district == '2':
        return "北京-通州"
    return 0


# 条件查询
@api_view(['GET'])
@permission_classes((AllowAny,))
def getPostListByBistrict(request, district=1):
    if request.method == 'GET':
        district_name = get_district_name(district)
        if district_name == 0:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        else:
            posts = Post.objects.filter(district=district_name)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 条件查询
@api_view(['GET'])
@permission_classes((AllowAny,))
def getPostListByVillage(request):
    if request.method == 'GET':
        village = request.GET.get('village')
        posts = Post.objects.filter(village=village)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 分页post列表
@api_view(['GET'])
@permission_classes((AllowAny,))
def getPostListByPage(request):
    if request.method == 'GET':
        post_list = Post.objects.all()
        paginator = Paginator(post_list, 1)  # 每页显示 25 个联系人
        page = request.GET.get('page')
        # post = Post.objects.get(pk=1)
        try:
            posts = paginator.page(page)
            serializer = PostSerializer(posts, many=True)
            return Response({"code": "200", "msg": "获得第" + page + "页的数据", "data": serializer.data})
        except PageNotAnInteger:
            # 如果用户请求的页码号不是整数，显示全部列表
            # images = StartInImage.objects.all()
            # serializer = StartInImageSerializer(images, many=True)
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            # return Response(serializer.data)
            return Response({"code": "200", "msg": "全部列表", "data": serializer.data})
        except EmptyPage:
            # 如果用户请求的页码号超过了最大页码号，显示最后一页
            posts = paginator.page(paginator.num_pages)
            serializer = PostSerializer(posts, many=True)
            return Response({"code": "200", "msg": "没有数据了", "data": []})
    return Response({"code": "205", "msg": "访问出错", "data": []})


# post列表,根据worker
@api_view(['GET'])
@permission_classes((AllowAny,))
def getPostListByWorker(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        worker_id = request.GET.get('workerId')
        # worker_id = 1
        if worker_id == None:
            return Response({"code": "205", "msg": "管家id无效", "data": []})
        worker_db = Worker.objects.get(pk=worker_id)
        worker_name = worker_db.name
        post_list = Post.objects.filter(worker=worker_db)
        # post_list = Post.objects.all()
        paginator = Paginator(post_list, 2)  # 每页显示 2 个联系人
        try:
            posts = paginator.page(page)
            serializer = PostSerializer(posts, many=True)

            # return Response(serializer.data)
            return Response({"code": "200", "msg": worker_name + "第" + page + "页的列表", "data": serializer.data})
        except PageNotAnInteger:
            # 如果用户请求的页码号不是整数，显示全部列表
            # images = StartInImage.objects.all()
            # serializer = StartInImageSerializer(images, many=True)
            # posts = Post.objects.all()
            serializer = PostSerializer(post_list, many=True)
            tt = serializer.data
            return Response({"code": "200", "msg": worker_name + "全部列表", "data": serializer.data})
        except EmptyPage:
            # 如果用户请求的页码号超过了最大页码号，显示最后一页
            # posts = paginator.page(paginator.num_pages)
            # serializer = PostSerializer(posts, many=True)
            return Response({"code": "200", "msg": "该页没有数据了", "data": []})
    return Response({"code": "205", "msg": "访问出错", "data": []})


# 增加新的post的接口
@api_view(['POST'])
@permission_classes((AllowAny,))  # 接口的访问权限设置http://www.django-rest-framework.org/api-guide/permissions/
def save_post(request):
    if request.method == 'POST':
        import json
        pp = request.POST
        data = request.data
        # files = request.FILES
        # 获得文件的个数
        file_dic = request.FILES.dict()
        res_json = data['res']
        post_dic = json.loads(res_json)  # 反序列化,将json串转为字典
        village = post_dic['village']
        district = post_dic['district']
        state = post_dic['state']
        predict = post_dic['predict']
        fact = post_dic['fact']
        worker_dic = post_dic['worker']
        worker_pk = worker_dic['pk']
        worker_db = Worker.objects.get(pk=worker_pk)
        service_dic = post_dic['service']
        service_name = service_dic['name']
        service = Service.objects.get(name=service_name)
        post = Post(village=village, created_time=timezone.now())
        post.service = service
        post.worker = worker_db
        post.state = state
        post.district = district
        post.predict = predict
        post.fact = fact
        post.save()
        for key, value in file_dic.items():
            k = key
            v = value
            if 'start_imag' in k:
                image = StartInImage(des=village + key, path=v)  # todo des字段里一定要有key,便于区分
                image.save()
                post.startinimage_set.add(image)  # todo 要先保存,然后才能做表之间的关联
            if 'protect_imag' in k:
                image = ProtectionImage(des=village + key, path=v)
                image.save()
                post.protectionimage_set.add(image)
            if 'work_site' in k:
                image = WorkSiteImage(des=village + key, path=v)
                image.save()
                post.worksiteimage_set.add(image)
            if 'finish' in k:
                image = FinishImage(des=village + key, path=v)
                image.save()
                post.finishimage_set.add(image)
            if 'head' in k:
                # todo 更新post的head字段,同时保存头图片
                post.post_imag = v
                post.save()
        list_post = []
        list_post.append(post)
        serializer = PostSerializer(list_post, many=True)
        # ff = serializer.data
        return Response({"code": "200", "msg": "上传成功", "photos": [], "data": serializer.data})
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({"code": "205", "msg": "上传失败", "photos": [], "data": []})


# 编辑已有的post的(包括上传图片)
@api_view(['POST'])
@permission_classes((AllowAny,))  # 接口的访问权限设置http://www.django-rest-framework.org/api-guide/permissions/
def update_post(request):
    if request.method == 'POST':
        import json
        pp = request.POST
        data = request.data
        # files = request.FILES
        # 获得文件的个数
        file_dic = request.FILES.dict()
        res_json = data['res']
        post_dic = json.loads(res_json)  # 反序列化,将json串转为字典
        pk = post_dic['pk']
        village = post_dic['village']
        # post = Post(village=village, created_time=timezone.now())
        post = Post.objects.get(pk=pk)
        post.village = post_dic['village']
        post.district = post_dic['district']
        post.created_time = timezone.now()
        post.predict = post_dic['predict']
        post.fact = post_dic['fact']
        post.state = post_dic['state']
        post.save()
        list_imag = []
        photo_list = []

        for key, value in file_dic.items():
            k = key
            v = value
            if 'start_imag' in k:
                image = StartInImage(des=pk + village + key, path=v)
                image.save()
                post.startinimage_set.add(image)  # todo 要先保存,然后才能做表之间的关联
                # todo 为了返回新上传的图片
                list_imag.append(image)
                serializer = StartInImageSerializer(list_imag, many=True)  # todo 将普通的list序列化
                photo_list = serializer.data  # todo 获得序列化之后的list
            if 'protect_imag' in k:
                image = ProtectionImage(des=pk + village + key, path=v)
                image.save()
                post.protectionimage_set.add(image)
                list_imag.append(image)
                serializer = ProtectionImageSerializer(list_imag, many=True)  # todo 将普通的list序列化
                photo_list = serializer.data  # todo 获得序列化之后的list
            if 'work_site' in k:
                image = WorkSiteImage(des=pk + village + key, path=v)
                image.save()
                post.worksiteimage_set.add(image)

                list_imag.append(image)
                serializer = WorkSiteImageSerializer(list_imag, many=True)  # todo 将普通的list序列化
                photo_list = serializer.data  # todo 获得序列化之后的list
            if 'finish' in k:
                image = FinishImage(des=pk + village + key, path=v)
                image.save()
                post.finishimage_set.add(image)
                list_imag.append(image)
                serializer = FinishImageSerializer(list_imag, many=True)  # todo 将普通的list序列化
                photo_list = serializer.data  # todo 获得序列化之后的list
            if 'head' in k:
                # todo 更新post的head字段,同时保存头图片
                post.post_imag = v
                post.save()
        post_serializer = PostSerializer(post,many=False)
        return Response({"code": "200", "msg": "上传成功", "photos": photo_list, "data": [],"post":post_serializer.data})
    return Response({"code": "205", "msg": "访问出错", "photos": [], "data": []})


# 获得post下的图组
@api_view(['GET'])
@permission_classes((AllowAny,))
def getPhotosByPost(request):
    if request.method == 'GET':
        try:
            pk = request.GET.get('postId')
            post_db = Post.objects.get(pk=pk)
            start_images = post_db.startinimage_set
            protection_images = post_db.protectionimage_set
            workesite_images = post_db.worksiteimage_set
            finish_iamges = post_db.finishimage_set

            start_images_serializer = StartInImageSerializer(start_images, many=True)
            protection_images_serializer = ProtectionImageSerializer(protection_images, many=True)
            worksite_images_serializer = WorkSiteImageSerializer(workesite_images, many=True)
            finish_images_serializer = FinishImageSerializer(finish_iamges, many=True)
            return Response({"code": "200", "msg": post_db.village + "图片租",
                             "startImages": start_images_serializer.data,
                             "protectionImages": protection_images_serializer.data,
                             "workSiteImages": worksite_images_serializer.data,
                             "finishImages": finish_images_serializer.data})
        except Exception:
            return Response({"code": "205", "msg": "访问出错"})
    return Response({"code": "205", "msg": "访问出错", "data": []})


# 删除指定图片组中的图片
@api_view(['GET'])
@permission_classes((AllowAny,))
def delete_photo(request):
    from django.core.files.storage import default_storage
    if request.method == 'GET':
        try:
            pk = request.GET.get('photoId')
            photoType = request.GET.get('photoType')
            k = photoType
            if 'start_imag' in k:
                image = StartInImage.objects.get(pk=pk)
                file = image.path  # todo 其实是一个Filed对象
                pp = file.path  # todo 获得Filed对象的全路径
                default_storage.delete(pp)  # todo 删掉了真正的文件
                image.delete()  # todo 删掉了数据库中的数据而已

            if 'protect_imag' in k:
                image = ProtectionImage.objects.get(pk=pk)
                file = image.path  # todo 其实是一个Filed对象
                pp = file.path  # todo 获得Filed对象的全路径
                default_storage.delete(pp)
                image.delete()
            if 'work_site' in k:
                image = WorkSiteImage.objects.get(pk=pk)
                file = image.path  # todo 其实是一个Filed对象
                pp = file.path  # todo 获得Filed对象的全路径
                default_storage.delete(pp)
                image.delete()
            if 'finish' in k:
                image = FinishImage.objects.get(pk=pk)
                file = image.path  # todo 其实是一个Filed对象
                pp = file.path  # todo 获得Filed对象的全路径
                default_storage.delete(pp)
                image.delete()
            return Response("删除成功")
        except Exception:
            return Response("删除失败")
    return Response("删除失败")


# worker登录验证
@api_view(['GET'])
@permission_classes((AllowAny,))
def login_worker(request):
    if request.method == "GET":
        try:
            tele = request.GET.get('telephone')
            password = request.GET.get('password')
            worker_db = Worker.objects.get(tele=tele)
            if worker_db is None:
                return Response({"code": "205", "msg": "未注册", "workers": []})
            if worker_db.password == password:
                # list_worker = []
                # list_worker.append(worker_db)
                serializer = WorkerSerializer(worker_db, many=False)
                ff= serializer.data
                return Response({"code": "200", "msg": "登录成功", "worker": ff})
            else:
                return Response({"code": "205", "msg": "密码错误", "workers": []})
        except Exception:
            return Response({"code": "305", "msg": "登录失败", "workers": []})
    return Response({"code": "305", "msg": "登录失败", "workers": []})

# worker修改密码
@api_view(['GET'])
@permission_classes((AllowAny,))
def new_password_worker(request):
    if request.method == "GET":
        try:
            tele = request.GET.get('telephone')
            new_password = request.GET.get('password')
            worker_db = Worker.objects.get(tele=tele)
            if worker_db is None:
                return Response({"code": "205", "msg": "未注册", "workers": []})
            if new_password is None:
                return Response({"code": "205", "msg": "修改失败", "workers": []})
            worker_db.password = new_password
            worker_db.save()
            # list_worker = []
            # list_worker.append(worker_db)
            # serializer = WorkerSerializer(list_worker,many=True)
            serializer = WorkerSerializer(worker_db, many=False) # todo 实现返回单独的对象
            return Response({"code": "200", "msg": "修改成功", "workers": [],"worker":serializer.data})
        except Exception:
            return Response({"code": "305", "msg": "修改失败", "workers": []})
    return Response({"code": "305", "msg": "修改失败", "workers": []})