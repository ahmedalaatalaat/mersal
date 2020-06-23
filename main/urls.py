from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cpanel.views_en import login_view as login_en
from cpanel.views_ar import login_view as login_ar
from cpanel.views_en import error_400, error_403, error_404, error_500
from django.conf.urls import handler400, handler403, handler404, handler500
from .admin import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cpanel/', include('cpanel.urls')),
    path('', login_en, name="login"),
    path('ar/', login_ar, name="ar_login"),
    path('api/', include('api.urls'))
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = error_400
handler403 = error_403
handler404 = error_404
handler500 = error_500
