from rest_framework import serializers, routers, viewsets
from .models import TodoItems
from member.models import Member
# from member.serializers import MemberSerializer
from django.contrib.auth.models import User 
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate 
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from django.utils import timezone

class MemberSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(
         allow_blank=True, allow_null=True
    )
    class Meta:
        db_table = ''
        model = Member
        managed = True
        verbose_name = 'member'
        verbose_name_plural = 'member'
        fields = ['user_id']

class TodoListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        db_table = '' 
        model = TodoItems
        managed = True
        verbose_name = 'TodoItems'
        verbose_name_plural = 'TodoItems'
        fields = ['id','title',
            'content', 'created_at','modified_at','completed', 'completed_at','due_date','user']
        
    def create(self, validated_data):

        user_object = validated_data.pop('user', None)
        tb = TodoItems.objects.create(
            title=validated_data['title'],
            content=validated_data['contents'],
            user= user_object
         
        )
        tb.save()
        return tb

class TodoListUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        db_table = ''
        model = TodoItems
        managed = True
        verbose_name = 'TodoItems'
        verbose_name_plural = 'TodoItems'
        fields = [
            # 'user_id',
            'completed',
            'completed_at',
        ]
    def update(self, instance, validated_data):

        todo = TodoItems.objects.get(pk=int(instance.id))
        todo.completed=validated_data['completed']
        if todo.completed:
            todo.completed_at = timezone.now() 
        else:
            todo.completed_at = None  
        todo.save()
        return todo
    
class TodoListSerializer(serializers.ModelSerializer):
    user = MemberSerializer(read_only = True, many = False)
    class Meta:
        db_table = '' 
        model = TodoItems
        managed = True
        verbose_name = 'TodoItems'
        verbose_name_plural = 'TodoItems'
        # fields = '__all__'
        fields = ['id','title',
            'content', 'created_at','modified_at','completed', 'completed_at','due_date','user']