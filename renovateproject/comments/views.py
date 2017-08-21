from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, detail_route
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from cases.models import Post

# Create your views here.
from comments.models import Comment, Owner
from comments.serializers import CommentSerializer, OwnerSerializer


@api_view(['GET'])
@permission_classes((AllowAny,))
def getCommentsInPost(request):
    if request.method == 'GET':
        try:
            pk = request.GET.get('postId')
            post_db = Post.objects.get(pk=pk)
            comments = post_db.comment_set

            comments_serializer = CommentSerializer(comments, many=True)
            return Response({"code": "200", "msg": post_db.village + "的评论",
                             "comments": comments_serializer.data
                             })
        except Exception:
            return Response({"code": "205", "msg": "访问出错1", "comments": []})
    return Response({"code": "205", "msg": "访问出错2", "comments": []})


@api_view(['POST'])
@permission_classes((AllowAny,))
def add_comment(request):
    if request.method == 'POST':
        try:
            import json
            pp = request.POST
            data = request.data
            param = data['param']
            comment_dic = json.loads(param)  # 反序列化,将json串转为字典
            post_pk = comment_dic['postId']
            owner_pk = comment_dic['ownerId']
            post_db = Post.objects.get(pk=post_pk)
            owner = post_db.owner

            if owner is None:
                return Response({"code": "205", "msg": "owner为空", "comments": []})
            if str(owner.pk) != owner_pk:
                return Response({"code": "206", "msg": "评论失败", "comments": []})
            # comment_name = comment_dic['name']
            comment_telephone = comment_dic['telephone']
            comment_text = comment_dic['text']

            new_comment = Comment()
            new_comment.post = post_db
            new_comment.worker = post_db.worker
            # new_comment.name = comment_name
            new_comment.telephone = comment_telephone
            new_comment.text = comment_text
            new_comment.save()
            ss = post_db.startinimage_set
            comments = post_db.comment_set.all()
            l = len(comments)
            comments_serializer = CommentSerializer(new_comment, many=False)
            return Response({"code": "200", "msg": post_db.village + "的评论",
                             "comment": comments_serializer.data, "comment_size": l
                             })
        except Exception:
            return Response({"code": "205", "msg": "访问出错1", "comments": []})
    return Response({"code": "205", "msg": "访问出错2", "comments": []})


# 添加回复
@api_view(['POST'])
@permission_classes((AllowAny,))
def add_call_back(request):
    if request.method == 'POST':
        # comment_id   post_id  worker_id
        try:
            import json
            data = request.data
            param = data['param']
            comment_dic = json.loads(param)  # 反序列化,将json串转为字典
            comment_pk = comment_dic['pk']
            call_back = comment_dic['call_back']
            comments = Comment.objects.filter(pk=comment_pk)
            if len(comments) > 0:
                comment = comments[0]
                ff = "fff"
                comment.call_back = call_back
                comment.save()
                # comment.objects.update(call_back=call_back)
                comments_serializer = CommentSerializer(comment, many=False)
                ff = "fff"
                return Response({"code": "200", "msg": "评论回复成功", "comment": comments_serializer.data})
            else:
                return Response({"code": "205", "msg": "评论不存在", "comments": []})
        except Exception:
            return Response({"code": "205", "msg": "访问出错1", "comments": []})
    return Response({"code": "205", "msg": "访问出错2", "comments": []})


@api_view(['GET'])
@permission_classes((AllowAny,))
def owner_login(request):
    if request.method == 'GET':
        try:
            telephone = request.GET.get('telephone')
            password = request.GET.get('password')
            owner_db = Owner.objects.filter(telephone=telephone, password=password)
            owner_serializer = OwnerSerializer(owner_db, many=True)
            return Response({"code": "200", "msg": telephone + "的业主",
                             "owners": owner_serializer.data
                             })
        except Exception:
            return Response({"code": "205", "msg": "访问出错1", "owners": []})
    return Response({"code": "205", "msg": "访问出错2", "owners": []})
