from rest_framework.routers import DefaultRouter
from barter.views import OfferViewSet, TradeableViewSet, ProposalViewSet
from django.urls import path, include

app_name = 'barter'

router = DefaultRouter()
router.register(r'offers', OfferViewSet, basename='offer')
router.register(r'proposals', ProposalViewSet, basename='proposal')
urlpatterns = [
    path('', include(router.urls)),
]
