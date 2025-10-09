# 代码生成时间: 2025-10-10 00:00:27
from datetime import datetime
from django.db import models
from django.urls import path
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
import hashlib


# 版权检测系统的模型
class Document(models.Model):
    """存储文档信息的模型"""
    title = models.CharField(max_length=255, help_text="文档标题")
    content = models.TextField(help_text="文档内容")
    created_at = models.DateTimeField(auto_now_add=True, help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, help_text="更新时间")
    hash_code = models.CharField(max_length=255, unique=True, blank=True, help_text="文档内容的哈希值")

    def save(self, *args, **kwargs):
        """保存文档时计算内容的哈希值"""
        if not self.hash_code:
            self.hash_code = hashlib.sha256(self.content.encode()).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# 版权检测系统的视图
class CopyrightDetectionView(View):
    """视图类，用于检测版权"""
    def post(self, request):
        "