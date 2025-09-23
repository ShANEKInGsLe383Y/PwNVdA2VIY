# 代码生成时间: 2025-09-23 12:21:47
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import statistics

# 定义模型
class DataPoint(models.Model):
    """模型代表数据点"""
    value = models.FloatField(help_text="数据值")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DataPoint(value={self.value})"

# 定义视图
@method_decorator(csrf_exempt, name='dispatch')
class DataAnalysisView(View):
    """视图处理数据点统计分析"""
    def post(self, request):
        """处理POST请求，计算统计数据"""
        if not request.POST.getlist('values'):
            return JsonResponse({'error': 'No data values provided'}, status=400)

        values = list(map(float, request.POST.getlist('values')))
        try:
            mean = statistics.mean(values)
            median = statistics.median(values)
            max_value = max(values)
            min_value = min(values)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

        return JsonResponse({
            'mean': mean,
            'median': median,
            'max': max_value,
            'min': min_value,
        })

# 定义URLs
data_analysis_urls = [
    path('analyze/', DataAnalysisView.as_view(), name='data_analysis'),
]

# 注意：在Django项目的urls.py中包含data_analysis_urls
# 例如：
# from django.urls import include, path
# urlpatterns = [
#     path('your_path/', include('your_app_name.urls')),
# ]
