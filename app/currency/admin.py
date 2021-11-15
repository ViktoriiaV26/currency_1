from django.contrib import admin

from currency.models import Source, ContactUs


class SourceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'source_url',
    )
    list_filter = (
        'name',
    )

    def has_delete_permission(self, request, obj=None):
        return False

    readonly_fields = (
        'source_url',
    )


admin.site.register(Source, SourceAdmin)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email_from',
        'subject',
        'message',
    )
    list_filter = (
        'email_from',
    )
    search_fields = (
        'email_from',
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(ContactUs, ContactUsAdmin)
