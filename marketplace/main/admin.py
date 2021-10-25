from django.contrib import admin

from .models import Banner


class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "created_date", "activity")


admin.site.register(Banner, BannerAdmin)
