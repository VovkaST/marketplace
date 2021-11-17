from django.contrib import admin
from profiles.models import Profile, UserAddress, ViewHistory


class ProfilesAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ["user", "phone_number", "patronymic"]


class UserAddressAdmin(admin.ModelAdmin):
    model = UserAddress
    list_display = ["country", "town", "region", "street", "apartment"]


class ViewHistoryAdmin(admin.ModelAdmin):
    model = ViewHistory
    list_display = ["user", "goods", "viewed_at"]
    ordering = ["viewed_at", "user"]


admin.site.register(Profile, ProfilesAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
admin.site.register(ViewHistory, ViewHistoryAdmin)
