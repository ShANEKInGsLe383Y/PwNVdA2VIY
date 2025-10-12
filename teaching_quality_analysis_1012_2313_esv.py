# 代码生成时间: 2025-10-12 23:13:37
from django.db import models
# 添加错误处理
from django.shortcuts import render, redirect
from django.views import View
from django.urls import path
from django.http import HttpResponse, JsonResponse
# NOTE: 重要实现细节
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import Course, Student, Teacher

# Models
class Course(models.Model):
    """Model representing a course."""
    name = models.CharField(max_length=100, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="courses")
    
    def __str__(self):
        return self.name

class Student(models.Model):
    """Model representing a student."""
# 增强安全性
    name = models.CharField(max_length=100)
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="students")
    
    def __str__(self):
# 添加错误处理
        return self.name

class Teacher(models.Model):
# 添加错误处理
    """Model representing a teacher."""
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

# Views
@method_decorator(login_required, name='dispatch')
class TeachingQualityAnalysisView(View):
    """View for analyzing teaching quality."""
    def get(self, request, *args, **kwargs):
        try:
            courses = Course.objects.all()
            return render(request, 'teaching_quality_analysis.html', {'courses': courses})
        except Exception as e:
            messages.error(request, str(e))
            return redirect('teaching_quality_analysis')

    @require_http_methods(['POST'])
    def post(self, request, *args, **kwargs):
        course_id = request.POST.get('course_id')
        try:
            course = Course.objects.get(id=course_id)
            students = course.students.all()
            grades = [student.grade for student in students]
            avg_grade = sum(grades) / len(grades) if grades else 0
            return JsonResponse({'avg_grade': avg_grade})
# 改进用户体验
        except ObjectDoesNotExist:
# 增强安全性
            return JsonResponse({'error': 'Course not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
# 优化算法效率

# URLs
urlpatterns = [
    path('teaching_quality_analysis/', TeachingQualityAnalysisView.as_view(), name='teaching_quality_analysis'),
]
