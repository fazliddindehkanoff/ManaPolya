from django.contrib import admin
from .models import Stadium, StadiumBooking, StadiumImages

class StadiumImagesInline(admin.TabularInline):  # or use `StackedInline`
    model = StadiumImages
    extra = 1  # Number of empty image fields to display

@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    inlines = [StadiumImagesInline]  # Add inline images inside the Stadium admin panel

admin.site.register(StadiumBooking)  # Keep this as a separate registration
