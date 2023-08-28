from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
 
urlpatterns = [
    path('', RedirectView.as_view(url='/bbs/')),
    path('index.html', RedirectView.as_view(url='/bbs/')),
    path('bbs/', include('bbs.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
]