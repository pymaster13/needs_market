"""foodmarket URL Configuration"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='NeedsMarketAPI')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_docs/', schema_view),
    path('api/v0/market/', include('market.urls', namespace='market')),
    path('api/v0/account/', include('account.urls', namespace='account')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
