from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/barter/', include('barter.urls')),
    path('api/accounts/', include('accounts.urls', namespace='accounts')),
]
