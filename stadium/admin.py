from django.contrib import admin
from .models import Stadium, StadiumImages

class StadiumImagesInline(admin.TabularInline):
    model = StadiumImages
    extra = 1
    

@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    inlines = [StadiumImagesInline]

