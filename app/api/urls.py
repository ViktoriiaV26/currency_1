from django.urls import path
from api.views import RatesView

app_name = 'api'

urlpatterns = [
    path('rates/', RatesView.as_view()),
]
