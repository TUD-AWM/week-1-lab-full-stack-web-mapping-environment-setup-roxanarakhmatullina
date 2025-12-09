# facilities/management/commands/load_osm_facilities.py

import json
import time
import requests

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point

from facilities.models import Facility


OSM_SPORT_TYPES = {
    "gym": ["amenity=gym", "leisure=fitness_centre"],
    "stadium": ["leisure=stadium"],
    "pitch": ["leisure=pitch"],
    "court": ["leisure=pitch"],
    "pool": ["leisure=swimming_pool"],
    "other": ["leisure=sports_centre", "leisure=track"],
}


class Command(BaseCommand):
    help = "Load sports facilities from OpenStreetMap (Overpass API) into the Facility table."

    def add_arguments(self, parser):
        parser.add_argument(
            "lat",
            type=float,
            help="Centre latitude (e.g. 53.3498 for Dublin)",
        )
        parser.add_argument(
            "lon",
            type=float,
            help="Centre longitude (e.g. -6.2603 for Dublin)",
        )
        parser.add_argument(
            "radius",
            type=int,
            help="Search radius in metres (e.g. 3000 for 3km).",
        )

    def handle(self, *args, **options):
        lat = options["lat"]
        lon = options["lon"]
        radius = options["radius"]

        self.stdout.write(
            self.style.NOTICE(
                f"Querying Overpass for facilities within {radius}m of ({lat}, {lon})..."
            )
        )

        # Build Overpass query
        # We request nodes with relevant tags around the given point
        or_parts = []
        for tag_list in OSM_SPORT_TYPES.values():
            for tag in tag_list:
                key, value = tag.split("=")
                or_parts.append(f'node["{key}"="{value}"](around:{radius},{lat},{lon});')

        query = f"""
        [out:json][timeout:25];
        (
            {"".join(or_parts)}
        );
        out body;
        """

        url = "https://overpass-api.de/api/interpreter"

        try:
            resp = requests.post(url, data={"data": query})
        except requests.RequestException as e:
            raise CommandError(f"Error calling Overpass API: {e}")

        if resp.status_code != 200:
            raise CommandError(
                f"Overpass API returned status {resp.status_code}: {resp.text[:200]}"
            )

        data = resp.json()
        elements = data.get("elements", [])

        created = 0
        skipped = 0

        for el in elements:
            if "lat" not in el or "lon" not in el:
                continue

            name = el.get("tags", {}).get("name")
            if not name:
                # Ignore unnamed features
                skipped += 1
                continue

            tags = el.get("tags", {})
            sport_type = self._guess_sport_type(tags)

            description_parts = []
            if "sport" in tags:
                description_parts.append(f"sport={tags['sport']}")
            if "leisure" in tags:
                description_parts.append(f"leisure={tags['leisure']}")
            if "amenity" in tags:
                description_parts.append(f"amenity={tags['amenity']}")
            description = ", ".join(description_parts) or "Imported from OpenStreetMap"

            lon_el = el["lon"]
            lat_el = el["lat"]

            # Create Point in WGS84
            point = Point(lon_el, lat_el, srid=4326)

            # Avoid obvious duplicates
            obj, was_created = Facility.objects.get_or_create(
                name=name,
                location=point,
                defaults={
                    "sport_type": sport_type,
                    "description": description,
                    "source": "osm",
                },
            )

            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported facilities from OSM. Created: {created}, skipped existing: {skipped}"
            )
        )

    def _guess_sport_type(self, tags):
        """
        Map OSM tags to our sport_type choices in Facility.
        """
        leisure = tags.get("leisure", "")
        amenity = tags.get("amenity", "")
        sport = tags.get("sport", "")

        if amenity == "gym" or "fitness" in leisure:
            return "gym"
        if leisure == "stadium":
            return "stadium"
        if leisure == "pitch":
            # Try to refine by sport
            if sport in {"tennis", "basketball"}:
                return "court"
            return "pitch"
        if leisure == "swimming_pool":
            return "pool"
        if leisure in {"sports_centre", "track"}:
            return "other"
        return "other"
