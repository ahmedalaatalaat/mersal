from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cpanel.views_en import login_view as login_en
from cpanel.views_ar import login_view as login_ar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cpanel/', include('cpanel.urls')),
    path('', login_en, name="login"),
    path('ar/', login_ar, name="ar_login"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
