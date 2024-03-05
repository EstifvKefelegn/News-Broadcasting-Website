from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _


urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path(_('admin/'), admin.site.urls),
 
]

urlpatterns += i18n_patterns(
    path('', include("News.urls")),
    path('users/', include('userauth.urls'))
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    