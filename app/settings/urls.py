from django.contrib import admin
from django.urls import path
from currency.views import hello_world, contactus_list

urlpatterns = [
    path('admin/', admin.site.urls),

    # currency
    path('contactus/list/', contactus_list),
    path('hello-world/', hello_world),
]
