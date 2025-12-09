from django.shortcuts import render
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.measure import D

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Facility, FacilityZone, Event
from .serializers import FacilitySerializer, FacilityZoneSerializer, EventSerializer

import json


class FacilityViewSet(viewsets.ModelViewSet):
    """
    Main API for facilities.
    - /api/facilities/               -> GeoJSON of all facilities (with optional sport_type + distance sorting)
    - /api/facilities/nearest/       -> nearest facility to ?lat=&lon=
    - /api/facilities/within_radius/ -> all facilities within radius ?lat=&lon=&km=
    - /api/facilities/in_bbox/       -> facilities inside bbox ?minx=&miny=&maxx=&maxy=
    """

    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer

    def get_queryset(self):
        qs = Facility.objects.all()
        sport = self.request.query_params.get("sport_type")
        lat = self.request.query_params.get("lat")
        lon = self.request.query_params.get("lon")

        if sport:
            qs = qs.filter(sport_type=sport)

        if lat and lon:
            try:
                user_location = Point(float(lon), float(lat), srid=4326)
                qs = qs.annotate(distance=Distance("location", user_location)).order_by("distance")
            except (TypeError, ValueError):
                # Ignore bad coordinates, just return unannotated queryset
                pass

        return qs

    def list(self, request, *args, **kwargs):
        """
        Return all facilities as a GeoJSON FeatureCollection so Leaflet can use it directly.
        """
        features = []
        for f in self.get_queryset():
            geo = json.loads(f.location.geojson)
            features.append(
                {
                    "type": "Feature",
                    "geometry": geo,
                    "properties": {
                        "id": f.id,
                        "name": f.name,
                        "description": f.description,
                        "sport_type": f.sport_type,
                        "source": f.source,
                    },
                }
            )

        return Response(
            {
                "type": "FeatureCollection",
                "features": features,
            }
        )

    @action(detail=False, methods=["get"])
    def nearest(self, request):
        """Return the single nearest facility to a given lat/lon."""
        try:
            lat = float(request.query_params.get("lat"))
            lon = float(request.query_params.get("lon"))
        except (TypeError, ValueError):
            return Response(
                {"error": "Provide ?lat=..&lon=.."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ref = Point(lon, lat, srid=4326)
        nearest = (
            self.get_queryset()
            .annotate(distance=Distance("location", ref))
            .order_by("distance")
            .first()
        )

        if not nearest:
            return Response({"type": "FeatureCollection", "features": []})

        feature = {
            "type": "Feature",
            "geometry": json.loads(nearest.location.geojson),
            "properties": {
                "id": nearest.id,
                "name": nearest.name,
                "description": nearest.description,
                "sport_type": nearest.sport_type,
                "source": nearest.source,
            },
        }
        return Response({"type": "FeatureCollection", "features": [feature]})

    @action(detail=False, methods=["get"])
    def within_radius(self, request):
        """Find all facilities within a radius (km) from lat/lon."""
        try:
            lat = float(request.query_params.get("lat"))
            lon = float(request.query_params.get("lon"))
            km = float(request.query_params.get("km", 5))
        except (TypeError, ValueError):
            return Response(
                {"error": "Provide ?lat=..&lon=..&km=.."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ref = Point(lon, lat, srid=4326)
        qs = (
            self.get_queryset()
            .filter(location__distance_lte=(ref, D(km=km)))
            .annotate(distance=Distance("location", ref))
            .order_by("distance")
        )

        features = []
        for f in qs:
            features.append(
                {
                    "type": "Feature",
                    "geometry": json.loads(f.location.geojson),
                    "properties": {
                        "id": f.id,
                        "name": f.name,
                        "description": f.description,
                        "sport_type": f.sport_type,
                        "source": f.source,
                        "distance_km": round(f.distance.km, 3),
                    },
                }
            )

        return Response({"type": "FeatureCollection", "features": features})

    @action(detail=False, methods=["get"])
    def in_bbox(self, request):
        """Return facilities inside a bounding box: ?minx=&miny=&maxx=&maxy= (lon/lat)."""
        try:
            minx = float(request.query_params.get("minx"))
            miny = float(request.query_params.get("miny"))
            maxx = float(request.query_params.get("maxx"))
            maxy = float(request.query_params.get("maxy"))
        except (TypeError, ValueError):
            return Response(
                {"error": "Provide ?minx=&miny=&maxx=&maxy="},
                status=status.HTTP_400_BAD_REQUEST,
            )

        poly = Polygon.from_bbox((minx, miny, maxx, maxy))
        poly.srid = 4326

        qs = self.get_queryset().filter(location__within=poly)

        features = []
        for f in qs:
            features.append(
                {
                    "type": "Feature",
                    "geometry": json.loads(f.location.geojson),
                    "properties": {
                        "id": f.id,
                        "name": f.name,
                        "description": f.description,
                        "sport_type": f.sport_type,
                        "source": f.source,
                    },
                }
            )

        return Response({"type": "FeatureCollection", "features": features})


class FacilityZoneViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API for polygon zones (coverage areas) in GeoJSON,
    so Leaflet can render them directly.

    /api/zones/ -> GeoJSON FeatureCollection
    """

    queryset = FacilityZone.objects.all()

    def list(self, request, *args, **kwargs):
        features = []

        for z in self.get_queryset():
            if not z.area:
                continue  # skip zones with no geometry

            geom = json.loads(z.area.geojson)
            features.append(
                {
                    "type": "Feature",
                    "geometry": geom,
                    "properties": {
                        "id": z.id,
                        "name": z.name,
                        "zone_type": z.zone_type,
                    },
                }
            )

        return Response(
            {
                "type": "FeatureCollection",
                "features": features,
            }
        )



class EventViewSet(viewsets.ModelViewSet):
    """
    CRUD / API for events attached to facilities.
    """

    queryset = Event.objects.select_related("facility").all()
    serializer_class = EventSerializer


def map_view(request):
    """
    Render the main Leaflet map page.
    """
    return render(request, "facilities_map.html")
