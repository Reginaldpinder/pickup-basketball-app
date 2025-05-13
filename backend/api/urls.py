from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GymViewSet, CourtViewSet, TeamViewSet, PlayerViewSet, ManagerViewSet

router = DefaultRouter()
router.register(r'gyms', GymViewSet)
router.register(r'courts', CourtViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'managers', ManagerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
