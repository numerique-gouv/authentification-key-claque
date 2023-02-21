from django.contrib import admin

from authentification.models import Client, RedirectUri


class RedirectUriInline(admin.TabularInline):
    model = RedirectUri


class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "client_id")
    inlines = [RedirectUriInline]


admin.site.register(Client, ClientAdmin)
