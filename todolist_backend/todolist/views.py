# parsing data from the client
from rest_framework.parsers import JSONParser
# To bypass having a CSRF token
from django.views.decorators.csrf import csrf_exempt
# for sending response to the client
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# API definition for task
from .serializers import TodoListSerializer,TodoListUpdateSerializer
# Task model
from .models import TodoItems

from rest_framework.views import APIView

from django.shortcuts import get_object_or_404, render

from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from django.db.models import Q
# from django.contrib.auth.models import User
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response # 사용자가 request를 하면 응답을 해줘야하기 때문에 Response 사용
from django.core.exceptions import ObjectDoesNotExist
from member.models import Member
import json 

class CreateView(viewsets.ModelViewSet): 
    queryset = TodoItems.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id == None:
            queryset = TodoItems.objects.order_by('-id').all()
        else:
            queryset = TodoItems.objects.filter(user=user_id).order_by('-id').all()
       
        return queryset
    
    def create(self, request):
        data = request.data
        print('data', data)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            member = get_object_or_404(Member, user_id = data.get('user_id'))
            serializer.save(user=member)

        return Response({
            'status': 200,
            'message': 'ok',
            'data': serializer.data
        })
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class DetailListView(generics.ListAPIView):
    serializer_class = TodoListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        progress = self.request.query_params.get('progress')
        user_id = self.kwargs.get('user_id')

        if user_id == None:
            queryset = TodoItems.objects.order_by('-id').all()
        else:
            print('yes')
            if progress == "inprogress":
                queryset = TodoItems.objects.filter(Q(user=user_id) & Q(completed=False)).order_by('-id').all()
            elif progress == "completed":
                queryset = TodoItems.objects.filter(Q(user=user_id) & Q(completed=True)).order_by('-id').all()
            else:
                queryset = TodoItems.objects.filter(user=user_id).order_by('-id').all()
     
        return queryset
    
class DetailView(generics.RetrieveUpdateAPIView):
    queryset = TodoItems.objects.all()
    serializer_class = TodoListUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get_queryset(self):
        return super().get_queryset()
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)