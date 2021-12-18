from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Open Rates API",
      default_version='v1',
      description="Current Bank Rates",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('django.contrib.auth.urls')),

    path('currency/', include('currency.urls')),
    path('accounts/', include('accounts.urls')),

    path('api/v1/', include('api.v1.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('__debug__/', include(debug_toolbar.urls)),

    # API docs
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
