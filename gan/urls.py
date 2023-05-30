from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from ganapp.signup import signup


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("ganapp.urls")),
    path('accounts/signup/', signup, name='account_signup'),
    path('accounts/', include('allauth.urls')),
    # other paths...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
