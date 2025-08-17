from django.urls import path
from .views import welcome_employer

urlpatterns = [
    path('', welcome_employer, name='welcome'),
    
]