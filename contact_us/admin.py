from django.contrib import admin
from .models import ContactUs

# Register your models here.

class ContactUsAdmin(admin.ModelAdmin):
    list_display=['id','name','phone','problem']
admin.site.register(ContactUs,ContactUsAdmin)