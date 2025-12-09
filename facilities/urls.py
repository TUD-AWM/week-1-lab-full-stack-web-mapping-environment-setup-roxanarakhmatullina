# facilities/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    FacilityViewSet,
    FacilityZoneViewSet,
    EventViewSet,
    map_view,
)

router = DefaultRouter()
router.register(r"facilities", FacilityViewSet, basename="facility")
router.register(r"zones", FacilityZoneViewSet, basename="facilityzone")
router.register(r"events", EventViewSet, basename="event")

urlpatterns = [
    path("map/", map_view, name="map"),
    path("", include(router.urls)),
]
