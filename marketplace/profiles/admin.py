from django.contrib import admin

from profiles.models import Profile, UserAddress


class ProfilesAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ["user", "phone_number", "patronymic"]


class UserAddressAdmin(admin.ModelAdmin):
    model = UserAddress
    list_display = ["country", "town", "region", "street", "apartment"]


admin.site.register(Profile, ProfilesAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
