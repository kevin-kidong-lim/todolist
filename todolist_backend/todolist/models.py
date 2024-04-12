from django.db import models
from django.urls import reverse

import random
import os
from member.models import Member
from django.utils.deconstruct import deconstructible

# Create your models here.
class TodoItems(models.Model):
    title = models.CharField(max_length=200,verbose_name='title')
    # user = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('member.Member', related_name="todouser", on_delete=models.DO_NOTHING, null=True, blank=True)
    content = models.TextField(max_length=200,null=True, blank=True,verbose_name='content')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='modified_at')
    completed = models.BooleanField(default=False, verbose_name='completed')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='completed_at')
    due_date = models.DateTimeField(null=True, blank=True, verbose_name='due_date')

    # def __str__(self):
    #     return self.title