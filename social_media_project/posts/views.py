from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Posts,TagWeight,PostImage
from user.models import Reacts
from django.db.models import Count,Case, CharField, Value, When
from django.conf import settings
import json
from rest_framework.permissions import IsAuthenticated




# Create your views here.
class PostViewSet(viewsets.ViewSet):
    """
     ViewSet for listing or create post.
    """
    permission_classes = [IsAuthenticated]
    def list(self, request):
        if request.user.is_staff:
            queryset = Posts.objects.values()
            for data in queryset:
                list_image=PostImage.objects.filter(fk_post_id=data['pk_bint_id']).values_list('images',flat=True)
                data['images']=['http://' + request.get_host()+settings.MEDIA_URL+imgdata for imgdata in list_image]
                data['weight'] = TagWeight.objects.filter(fk_post_id=data['pk_bint_id']).values('tag','weight')
            return Response({"status":True,"data":queryset})
        else:
            return Response({"status": True, "message": "Not allowed"})


    def create(self, request):
        try:
            if not request.user.is_staff:
                return Response({"status": True, "message": "Not allowed"})
            if request.data:
                insPost=Posts.objects.create(title=request.data['title'] , description=request.data['description'])
                if insPost and request.data['images']:
                    images= dict((request.data).lists())['images']
                    for data in images:
                        PostImage.objects.create(fk_post=insPost,images=data)
                if insPost and request.data['weight']:
                    weight_dict=json.loads(request.data['weight'])
                    lst_tag=[]
                    for key in weight_dict:
                        lst_tag.append(TagWeight(fk_post=insPost,tag=key,weight=weight_dict[key]))
                    TagWeight.objects.bulk_create(lst_tag)
            print(request.data)
            return Response({"status": True})
        except Exception as e:
            return Response({'status': False, 'data': 'Something Went Wrong'})

class PostLikesViewSet(viewsets.ViewSet):
    """
         ViewSet for likes of a post.
        """
    permission_classes = [IsAuthenticated]
    def list(self, request):
        try:
            if not request.user.is_staff:
                return Response({"status": True, "message": "Not allowed"})
            if 'id' not in request.GET:
                return Response({"status": True, "message": 'please provide post id'})
            if request.GET and  request.GET['id']:
                process_id=int(request.GET['id'])
                queryset = Posts.objects.filter(pk_bint_id=process_id).values()
                if queryset:
                    list_image = PostImage.objects.filter(fk_post_id=process_id).values_list('images', flat=True)
                    queryset[0]['images'] = ['http://' + request.get_host() + settings.MEDIA_URL + imgdata for imgdata in list_image]
                    queryset[0]['weight'] = TagWeight.objects.filter(fk_post_id=process_id).values('tag', 'weight')
                    dct_react=Reacts.objects.filter(fk_post_id=process_id).annotate( reaction=Case(When(react = True, then = Value('like')),When(react = False, then = Value('dislike')),output_field = CharField())).values('reaction').annotate(count=Count('reaction')).values_list('reaction','count')
                    if dct_react:
                        queryset[0]['reaction_count']=dict(dct_react)
                    else:
                        queryset[0]['reaction_count'] = {'like':0,'dislike':0}
                    return Response({"status": True, "data": queryset})
                else:
                    return Response({"status": True, "Message": "Please provide a valid post id "})

            else:
                return Response({"status": True, "data": "No id has been given as query"})
        except Exception as e:
            return Response({'status': False, 'data': 'Something Went Wrong'})