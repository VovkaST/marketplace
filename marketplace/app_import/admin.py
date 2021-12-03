from django.contrib import admin

from app_import.models import ImportProtocol


@admin.register(ImportProtocol)
class ImportProtocolAdmin(admin.ModelAdmin):
    pass
