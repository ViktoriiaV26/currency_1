from django.urls import path

from api import views
from rest_framework.routers import DefaultRouter


app_name = 'api'
router = DefaultRouter()
router.register(r'rates', views.RateViewSet, basename='rate')

urlpatterns = [
    # path('rates/', views.RatesView.as_view()),
    # path('rates/<int:pk>/', views.RateDetailsView.as_view()),
]
urlpatterns.extend(router.urls)