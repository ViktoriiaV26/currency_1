from django.contrib import admin
from django.urls import path
from currency.views import index, hello_world, contactus_list, rate_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),

    # currency
    path('rate/list/', rate_list),
    path('contactus/list/', contactus_list),
    path('hello-world/', hello_world),
]
