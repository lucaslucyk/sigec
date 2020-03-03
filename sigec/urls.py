"""sigec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from apps.saas import views as saasviews

urlpatterns = [
    re_path(r'^admin/dynamic_raw_id/', include('dynamic_raw_id.urls')),
    path('create_offer/', saasviews.offer_create, name="offer_create"),
    path('get_precios/<str:tipo_venta>/<str:plan>/<str:hardware>/<str:modulos>/<int:empleados>/', saasviews.get_precios, name="get_precios"),

    path('', admin.site.urls),
    #path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
