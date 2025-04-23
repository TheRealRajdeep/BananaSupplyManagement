# ml/urls.py
from django.urls import path
from .views import PredictRipenessView

urlpatterns = [
    path('predict-ripeness/', PredictRipenessView.as_view(), name='predict-ripeness'),
]