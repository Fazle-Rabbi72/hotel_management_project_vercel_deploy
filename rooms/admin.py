from django.contrib import admin
from .models import Room
# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    list_display=['id','hotel','room_type','price_per_night','is_available']
admin.site.register(Room,RoomAdmin)