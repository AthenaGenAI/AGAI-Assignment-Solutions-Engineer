from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ...existing URL patterns...
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])