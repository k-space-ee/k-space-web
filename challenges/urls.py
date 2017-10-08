"""challenges URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from challenges import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login_view),
    url(r'^logout/', views.logout_view),
    url(r'^register/', views.register),
    url(r'^challenge/(?P<id>[0-9]+)', views.challenge),
    url(r'^challenges/', views.challenges),
    url(r'^halloffame/', views.hall_of_fame),
    url(r'^profile/(?P<username>[\w.-]+)', views.profile),
    url(r'^favicon.ico$', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'), permanent=False), name='favicon')
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

