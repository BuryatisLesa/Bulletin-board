"""
URL configuration for BulletinBoard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from board import views
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckeditor_views

router = routers.DefaultRouter()
router.register(r'boards', views.BoardViewset)
router.register(r'users', views.UserViewSet)
router.register(r'categories', views.CategoryViewset)
router.register(r'responsesboards', views.ResponseViewset)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('board.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('i18n/', include('django.conf.urls.i18n')),
    # ckeditor
    # re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # add images and videos only auth users(login_required)
    re_path(r'^ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
    re_path(r'^ckeditor/browse/', login_required(ckeditor_views.browse), name='ckeditor_browse'),
]

# lock in dev
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
