from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User as AuthUser
from django.conf import settings
from .models import Reacts
from posts.models import Posts,TagWeight,PostImage
import requests
import json
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count,Case, CharField, Value, When,Sum
import datetime



# Create your views here.
class ListUserViewSet(viewsets.ViewSet):
    """
     ViewSet for listing  users.
    """
    permission_classes = [IsAuthenticated]
    def list(self, request):
        print(request.user)
        if request.user.is_staff:
            queryset = list(AuthUser.objects.values())
        else:
            queryset = list(AuthUser.objects.filter(id=request.user.id).values())

        return Response({"status":True,"data":queryset})


class UserViewSet(viewsets.ViewSet):
    """
    A  ViewSet for create users.
    """
    # permission_classes = [IsAuthenticated]
    def create(self, request):
        try:
            if request.data:
                try:
                    insUser=AuthUser.objects.create_user(request.data['username'] ,request.data['username'],request.data['password'])
                except Exception as e:
                    return Response({'status': False, 'data': 'User creation failed please do it with other email'})
                if insUser:
                    token_json = requests.post('http://' + request.get_host() + '/api-token-auth/',
                                               {'username': request.data['username'], 'password': request.data['password']})
                    token = json.loads(token_json._content.decode("utf-8"))['token']
            return Response({"status": True,'token':token})
        except Exception as e:
            return Response({'status': False, 'data': 'Something Went Wrong'})

class ReactViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for react managements.
    """
    permission_classes = [IsAuthenticated]
    def list(self, request):
        try:
            print(request.user)
            if request.user.is_staff:
                queryset = list(Posts.objects.values())
            else:
                lst_return=[]
                last_reacted=Reacts.objects.filter(fk_user_id=request.user.id).order_by('-timestamp').values('fk_post_id','react')
                if(last_reacted):

                    weightData=TagWeight.objects.filter(fk_post_id=last_reacted[0]['fk_post_id']).order_by('-weight').values_list('tag',flat=True)
                    data_check = ''.join(weightData)
                    total_list=TagWeight.objects.exclude(fk_post_id=last_reacted[0]['fk_post_id']).order_by('fk_post_id','-weight').values()
                    if total_list:
                        temp_list=[total_list[0]['tag']]
                        predict_list=[]
                        temp_post_id=total_list[0]['fk_post_id']
                        for data in total_list[1:]:
                            if temp_post_id==data['fk_post_id']:
                                temp_list.append(data['tag'])
                            else:
                                data_string=''.join(temp_list)
                                if data_string.find(data_check)==-1:
                                    temp_post_id = data['fk_post_id']
                                    temp_list = [data['tag']]
                                else:
                                    predict_list.append(temp_post_id)
                                    temp_post_id=data['fk_post_id']
                                    temp_list = [data['tag']]

                        if last_reacted[0]['react']:
                            lst_return.extend(Posts.objects.filter(pk_bint_id__in=predict_list).exclude(pk_bint_id=last_reacted[0]['fk_post_id']).values())
                            lst_return.extend(Posts.objects.exclude(pk_bint_id__in=predict_list).exclude(pk_bint_id=last_reacted[0]['fk_post_id']).values())
                        else:
                            lst_return.extend(Posts.objects.exclude(pk_bint_id__in=predict_list).exclude(pk_bint_id=last_reacted[0]['fk_post_id']).values())
                            lst_return.extend(Posts.objects.filter(pk_bint_id__in=predict_list).exclude(pk_bint_id=last_reacted[0]['fk_post_id']).values())
                        for data in lst_return:
                            list_image = PostImage.objects.filter(fk_post_id=data['pk_bint_id']).values_list('images',flat=True)
                            data['images'] = ['http://' + request.get_host() + settings.MEDIA_URL + imgdata for imgdata in list_image]
                            data['weight'] = TagWeight.objects.filter(fk_post_id=data['pk_bint_id']).values('tag','weight')
                    else:
                        return Response({"status": True, "data": lst_return})
                else:
                    lst_return=(Posts.objects.values())
                    for data in lst_return:
                        list_image = PostImage.objects.filter(fk_post_id=data['pk_bint_id']).values_list('images',flat=True)
                        data['images'] = ['http://' + request.get_host() + settings.MEDIA_URL + imgdata for imgdata in list_image]
                        data['weight'] = TagWeight.objects.filter(fk_post_id=data['pk_bint_id']).values('tag', 'weight')
            return_data=paginate(lst_return)
            return Response({"status":True,"data":return_data})
        except Exception as e:
            return Response({'status': False, 'data': 'Something Went Wrong'})

    def create(self, request):
        try:
            if request.data:
                try:
                    if 'post_id' not in request.data:
                        return Response({"status": True, "message": 'please provide post id'})
                    if 'reaction' not in request.data:
                        return Response({"status": True, "message": 'please provide reaction'})

                    insReact = Reacts.objects.filter(fk_post_id=request.data['post_id'],fk_user_id=request.user.id)
                    if insReact:
                        insReact.update(react=request.data['reaction'],timestamp=datetime.datetime.now())
                    else:
                        insReact = Reacts.objects.create(fk_post_id=request.data['post_id'], fk_user_id=request.user.id,
                                                        react=request.data['reaction'],timestamp=datetime.datetime.now())
                    return Response({"status": True, "message": 'successfully reacted'})
                except Exception as e:
                    return Response({'status': False, 'message': 'reacting on post was failed'})
            else:
                return Response({"status": True, "message": 'please provide post id'})


        except Exception as e:
            return Response({'status': False, 'data': 'Something Went Wrong'})

class PostLikesViewSet(viewsets.ViewSet):
    """
     ViewSet for get users who  reacts to a post.
    """
    permission_classes = [IsAuthenticated]
    def list(self, request):
        try:
            if 'id' not in request.GET:
                return Response({"status": True, "message": 'please provide post id'})
            if request.GET and  request.GET['id']:
                process_id=int(request.GET['id'])
                queryset = Posts.objects.filter(pk_bint_id=process_id).values()
                if queryset:
                    list_image = PostImage.objects.filter(fk_post_id=process_id).values_list('images', flat=True)
                    queryset[0]['images'] = ['http://' + request.get_host() + settings.MEDIA_URL + imgdata for imgdata in list_image]
                    queryset[0]['weight'] = TagWeight.objects.filter(fk_post_id=process_id).values('tag', 'weight')
                    dct_react=Reacts.objects.filter(fk_post_id=process_id).values('fk_user__username','fk_user__email').distinct('fk_user_id')

                    if dct_react:
                        react_users=[{'name':data['fk_user__username'],'email':data['fk_user__email']}  for data in dct_react]
                        queryset[0]['reacted_users']=react_users
                    else:
                        queryset[0]['reacted_users'] = []
                    return Response({"status": True, "data": queryset})
                else:
                    return Response({"status": True, "Message": "Please provide a valid post id "})

            else:
                return Response({"status": True, "data": "No id has been given as query"})
        except Exception as e:
            return Response({'status': False, 'data': 'Something Went Wrong'})

def paginate(data):
    print(data)
    dct_return={}
    index=1
    dct_return[index] = []
    for count, insdata in enumerate(data,1):
        if count%10==0:
            index+=1
            dct_return[index]=[]
        dct_return[index].append(insdata)
    return dct_return