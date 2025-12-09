from rest_framework import serializers
from .models import Facility, FacilityZone, Event


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = (
            "id",
            "name",
            "description",
            "sport_type",
            "location",
            "source",
            "created_at",
            "updated_at",
        )


class FacilityZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityZone
        fields = (
            "id",
            "name",
            "sport_type",
            "area",
            "description",
            "created_at",
            "updated_at",
        )


class EventSerializer(serializers.ModelSerializer):
    facility_name = serializers.CharField(source="facility.name", read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "facility",
            "facility_name",
            "title",
            "description",
            "start_time",
            "end_time",
            "created_at",
        )
