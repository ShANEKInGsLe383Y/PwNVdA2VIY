# 代码生成时间: 2025-10-03 18:54:38
from django.db import models
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


# Models
class Product(models.Model):
# 增强安全性
    """Model representing a product in the cross-border e-commerce platform."""
    name = models.CharField(max_length=255, help_text="Product name")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Product price")
    stock = models.IntegerField(default=0, help_text="Product stock")
    created_at = models.DateTimeField(default=timezone.now, help_text="Creation time")
# NOTE: 重要实现细节
    updated_at = models.DateTimeField(auto_now=True, help_text="Update time")

    def __str__(self):
        return self.name

# Views
@method_decorator(csrf_exempt, name='dispatch')
class ProductListView(View):
# 优化算法效率
    """View to list all products."""
# 扩展功能模块
    def get(self, request):
        """Handle GET request to list all products."""
        products = Product.objects.all()
        return JsonResponse(list(products.values()), safe=False)

    def post(self, request):
        """Handle POST request to create a new product."""
        data = request.POST
        try:
            product = Product.objects.create(
                name=data.get('name'),
                price=data.get('price'),
                stock=data.get('stock')
            )
            product.save()
            return JsonResponse({'id': product.id, 'name': product.name}, status=201)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ProductDetailView(View):
# 扩展功能模块
    """View to detail a specific product."""
    def get(self, request, pk):
        """Handle GET request to detail a specific product."""
        try:
# NOTE: 重要实现细节
            product = Product.objects.get(pk=pk)
            return JsonResponse(product.__dict__)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

    def put(self, request, pk):
        """Handle PUT request to update a specific product."""
        data = request.PUT
        try:
            product = Product.objects.get(pk=pk)
            product.name = data.get('name', product.name)
            product.price = data.get('price', product.price)
            product.stock = data.get('stock', product.stock)
# 增强安全性
            product.save()
            return JsonResponse(product.__dict__)
        except Product.DoesNotExist:
# FIXME: 处理边界情况
            return JsonResponse({'error': 'Product not found'}, status=404)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, pk):
        """Handle DELETE request to delete a specific product."""
# NOTE: 重要实现细节
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return HttpResponse(status=204)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

# URLs
urlpatterns = [
# 优化算法效率
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
# FIXME: 处理边界情况
]
# NOTE: 重要实现细节
