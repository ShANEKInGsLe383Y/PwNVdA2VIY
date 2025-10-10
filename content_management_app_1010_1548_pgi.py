# 代码生成时间: 2025-10-10 15:48:11
from django.db import models
from django.utils import timezone
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

"""
内容管理系统应用组件
"""

class Content(models.Model):
    """
    内容模型
    """
    title = models.CharField(max_length=200, help_text="标题")
    content = models.TextField(help_text="内容")
    created_at = models.DateTimeField(auto_now_add=True, help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, help_text="更新时间")

    def __str__(self):
        return self.title

class ContentView(View):
    """
    内容视图
    """
    def get(self, request, *args, **kwargs):
        try:
            content = Content.objects.all()
            return render(request, 'content_list.html', {'content_list': content})
        except Exception as e:
            raise Http404("内容列表获取失败")

    def post(self, request, *args, **kwargs):
        try:
            title = request.POST.get('title')
            content = request.POST.get('content')
            Content.objects.create(title=title, content=content)
            return render(request, 'content_list.html')
        except Exception as e:
            raise Http404("内容创建失败")

@method_decorator(csrf_protect, name='dispatch')
class ContentDetailView(View):
    """
    内容详情视图
    """
    def get(self, request, pk, *args, **kwargs):
        try:
            content = get_object_or_404(Content, pk=pk)
            return render(request, 'content_detail.html', {'content': content})
        except Http404:
            return render(request, 'error.html', {'error_message': '内容不存在'})
        except Exception as e:
            raise Http404("内容详情获取失败")

    def put(self, request, pk, *args, **kwargs):
        try:
            content = get_object_or_404(Content, pk=pk)
            title = request.PUT.get('title')
            content = request.PUT.get('content')
            content.title = title
            content.save()
            return render(request, 'content_detail.html', {'content': content})
        except Http404:
            return render(request, 'error.html', {'error_message': '内容不存在'})
        except Exception as e:
            raise Http404("内容更新失败")

    def delete(self, request, pk, *args, **kwargs):
        try:
            content = get_object_or_404(Content, pk=pk)
            content.delete()
            return render(request, 'content_list.html')
        except Http404:
            return render(request, 'error.html', {'error_message': '内容不存在'})
        except Exception as e:
            raise Http404("内容删除失败")

urlpatterns = [
    path('content/', ContentView.as_view(), name='content_list'),
    path('content/<int:pk>/', ContentDetailView.as_view(), name='content_detail')
]