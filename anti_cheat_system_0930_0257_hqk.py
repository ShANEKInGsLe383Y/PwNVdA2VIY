# 代码生成时间: 2025-09-30 02:57:27
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.exceptions import ValidationError
import hashlib
import json


# Anti-cheat models
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    last_login_attempt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username


class LoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.CharField(max_length=15)
    user_agent = models.CharField(max_length=255)
    success = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"


# Anti-cheat views
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    """
    A view to handle user logins and detect potential cheating attempts.
    """
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to login a user.
        """
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            ip_address = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT')

            # Validate user credentials and IP address
            user = User.objects.get(username=username)
            if user.password == hashlib.sha256(password.encode()).hexdigest():
                LoginAttempt.objects.create(
                    user=user,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    success=True
                )
                return JsonResponse({'status': 'success'}, status=200)

            # Record failed login attempt
            LoginAttempt.objects.create(
                user=user,
                ip_address=ip_address,
                user_agent=user_agent,
                success=False
            )
            raise ValidationError('Invalid credentials')

        except User.DoesNotExist:
            return JsonResponse({'status': 'User does not exist'}, status=404)
        except ValidationError as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# Anti-cheat URL configuration
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]
