from django.db import models
from django.contrib.gis.db import models as gis_models


class Facility(models.Model):
    SPORT_CHOICES = [
        ("gym", "Gym"),
        ("rink", "Ice Rink"),
        ("stadium", "Stadium"),
        ("pool", "Swimming Pool"),
        ("court", "Court"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    sport_type = models.CharField(max_length=50, choices=SPORT_CHOICES, default="other")
    # PointField for map location
    location = gis_models.PointField(geography=True)

    # Extra metadata (used by the OSM import)
    source = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="osm",
        help_text="Where this facility came from (e.g. osm, manual).",
    )
    external_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="ID from an external API such as Overpass/OSM.",
    )
    external_source = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Name of the external data source.",
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class FacilityZone(models.Model):
    ZONE_TYPE_CHOICES = [
        ("city", "City"),
        ("district", "District"),
        ("safety", "Safety Zone"),
        ("coverage", "Coverage Area"),
    ]

    name = models.CharField(max_length=255)
    zone_type = models.CharField(
        max_length=50,
        choices=ZONE_TYPE_CHOICES,
        default="coverage",
    )
    # Allow null so Django doesn’t ask you for a default in migrations
    area = gis_models.PolygonField(geography=True, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.zone_type})"


class Event(models.Model):
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="events",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    sport_tag = models.CharField(max_length=50, blank=True)
    is_live = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
