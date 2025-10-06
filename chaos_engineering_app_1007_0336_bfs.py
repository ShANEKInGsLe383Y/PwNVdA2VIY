# 代码生成时间: 2025-10-07 03:36:23
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChaosExperiment
from django.utils.decorators import method_decorator
from django.db.models import Q
import random
import logging

# Create your views here.

class ChaosEngineeringView(View):
    def get(self, request):
        """
        Get all chaos experiments.
        """
        experiments = ChaosExperiment.objects.all()
        return JsonResponse(list(experiments.values()), safe=False)
    
    def post(self, request):
        """
        Create a new chaos experiment.
        """
        data = request.POST
        try:
            experiment_name = data.get('name')
            experiment_type = data.get('type')
            ChaosExperiment.objects.create(name=experiment_name, type=experiment_type)
            return JsonResponse({'message': 'Experiment created successfully.'}, status=201)
        except Exception as e:
            logging.error(f'Failed to create experiment: {e}')
            return JsonResponse({'error': 'Failed to create experiment.'}, status=400)

    def delete(self, request, experiment_id):
        """
        Deletes a chaos experiment by ID.
        """
        try:
            ChaosExperiment.objects.get(id=experiment_id).delete()
            return JsonResponse({'message': 'Experiment deleted successfully.'})
        except ChaosExperiment.DoesNotExist:
            return JsonResponse({'error': 'Experiment not found.'}, status=404)
        except Exception as e:
            logging.error(f'Failed to delete experiment: {e}')
            return JsonResponse({'error': 'Failed to delete experiment.'}, status=500)

# Models
class ChaosExperiment(models.Model):
    """
    Represents a chaos experiment.
    """
    name = models.CharField(max_length=255, blank=False)
    type = models.CharField(max_length=255, blank=False)
    
    def __str__(self):
        return self.name

# URLs
from django.urls import path

urlpatterns = [
    path('chaos-experiments/', ChaosEngineeringView.as_view(), name='chaos_experiments'),
]
