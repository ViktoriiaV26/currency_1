from django.urls import path
from currency.views import (
                  RateListView, ContactUsListView, ContactUsCreateView,
                  SourceListView, SourceCreateView, SourceDetailView, SourceUpdateView, SourceDeleteView,)


app_name = 'currency'

urlpatterns = [
    path('rate/list/', RateListView.as_view(), name='rate-list'),
    path('source/list/', SourceListView.as_view(), name='source-list'),
    path('source/create/', SourceCreateView.as_view(), name='source-create'),
    path('source/details/<int:pk>/', SourceDetailView.as_view(), name='source-details'),
    path('source/update/<int:pk>/', SourceUpdateView.as_view(), name='source-update'),
    path('source/delete/<int:pk>/', SourceDeleteView.as_view(), name='source-delete'),
    path('contactus/list/', ContactUsListView.as_view(), name='contactus-list'),
    path('contactus/create/', ContactUsCreateView.as_view(), name='contactus-create'),

]
