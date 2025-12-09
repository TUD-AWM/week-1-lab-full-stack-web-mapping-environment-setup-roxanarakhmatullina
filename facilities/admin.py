from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import Facility, FacilityZone, Event
from .forms import FacilityForm



@admin.register(Facility)
class FacilityAdmin(GISModelAdmin):
    form = FacilityForm          # if you have this; remove line if not
    list_display = ("name", "sport_type", "location")
    search_fields = ("name", "description")
    list_filter = ("sport_type",)

@admin.register(FacilityZone)
class FacilityZoneAdmin(GISModelAdmin):
   
    list_display = ("id",)
   

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    
    list_display = ("id",)





