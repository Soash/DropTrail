from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler404
from accounts.views import custom_404
from django.conf import settings
from django.conf.urls.static import static

handler404 = custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('shop.urls')),
    path('', include('payment.urls')),
    path('', include('info.urls')),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




