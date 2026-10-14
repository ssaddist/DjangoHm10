from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CharacterViewSet, BattleSimulationView, BattleViewSet

router = DefaultRouter()
router.register('characters', CharacterViewSet, basename='character')
router.register('battles', BattleViewSet, basename='battle')

urlpatterns = [
    path('battle/', BattleSimulationView.as_view(), name='battle-simulation'),
    path('', include(router.urls)),
]
