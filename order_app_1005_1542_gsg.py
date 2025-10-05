# 代码生成时间: 2025-10-05 15:42:36
from django.db import models
from django.shortcuts import render, redirect
from django.urls import path
from django.http import HttpResponse
from django.views import View
from django.views.decorators.http import require_http_methods

# Model for Order
class Order(models.Model):
    """Order model for storing order details"""
    order_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    status = models.CharField(max_length=100, default='pending')

    def __str__(self):
        return f"Order {self.order_id} - {self.product_name}"

# View for handling order process
class OrderProcessView(View):
    """View class for processing orders"""

    @require_http_methods(['GET', 'POST'])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Handle GET request to display order form"""
        return render(request, 'order_form.html')

    def post(self, request, *args, **kwargs):
        """Handle POST request to process the order"""
        try:
            customer_name = request.POST.get('customer_name')
            product_name = request.POST.get('product_name')
            quantity = int(request.POST.get('quantity'))

            if not (customer_name and product_name and quantity):
                raise ValueError("Missing order details")

            order = Order.objects.create(
                customer_name=customer_name,
                product_name=product_name,
                quantity=quantity
            )

            # Process order logic here (e.g., validate stock, payment processing)
            # For simplicity, we assume all orders are valid

            return redirect('order_success', order_id=order.order_id)
        except ValueError as e:
            return HttpResponse(f"Error: {str(e)}", status=400)
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

# URL configuration for the order app
urlpatterns = [
    path('order/', OrderProcessView.as_view(), name='order_process'),
    path('order-success/<int:order_id>/', OrderSuccessView.as_view(), name='order_success'),
]

# View for displaying order success page
class OrderSuccessView(View):
    """View for displaying the order success page"""
    def get(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(order_id=order_id)
            return render(request, 'order_success.html', {'order': order})
        except Order.DoesNotExist:
            return HttpResponse("Order not found", status=404)
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)