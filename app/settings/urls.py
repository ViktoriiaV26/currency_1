from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('django.contrib.auth.urls')),

    path('currency/', include('currency.urls')),
    path('accounts/', include('accounts.urls')),

    path('api/', include('api.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('__debug__/', include(debug_toolbar.urls)),
]
urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
