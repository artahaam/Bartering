from rest_framework.routers import DefaultRouter
from barter.views import OfferViewSet, TradeableViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'offers', OfferViewSet)
router.register(r'currencies', TradeableViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
