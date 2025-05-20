from rest_framework.routers import DefaultRouter
from exchange.views import OfferViewSet, CurrencyViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'offers', OfferViewSet)
router.register(r'currencies', CurrencyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
