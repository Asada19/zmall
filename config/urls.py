"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from advertisement.views import index, index_detail


schema_view = get_schema_view(
    openapi.Info(
          title="Snippets API",
          default_version='v1',
          description="Test description",
    ),
    public=True
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', index, name='home'),
    # path('ad/<int:pk>', IndexDetail.as_view(), name='ad_detail'),
    path('ad/<int:pk>', index_detail, name='ad_detail'),
    path('accounts/', include('user.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('advertisement.urls')),
    path('api/', include('helpers.urls')),
    path('api/auth/', include('api_auth.urls')),
    path('api/', include('chat.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
