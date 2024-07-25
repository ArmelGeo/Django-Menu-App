from django.urls import path
from .views import HomePageView

urlpatterns = [
    path('menu/', HomePageView.as_view(), name='home'),
]
