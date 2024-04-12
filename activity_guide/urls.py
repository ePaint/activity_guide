from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from activity_guide import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('categories/', include('categories.urls')),
    path('providers/', include('providers.urls')),
    path('activities/', include('activities.urls')),
    path('members/', include('members.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ads/', include('ads.urls')),
    path('', include('layout.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'layout.views.not_found'
handler500 = 'layout.views.server_error'
