from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION


admin.site.site_header = "Mersal Administration"
admin.site.site_title = "Mersal Administration"


class LogEntry_admin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    readonly_fields = [f.name for f in LogEntry._meta.get_fields()]
    list_display = [
        'id',
        'done_by_id',
        'done_by_username',
        'content_type',
        'action_flag_',
        'done_on_id',
        'action',
        'change_message',
        'action_time',
    ]

    list_filter = [
        'content_type',
        'action_flag',
        'action_time'
    ]

    # search_fields = ('user', 'user__first_name', )
    search_fields = [
        'user__id__exact',
        'user__username__exact',
        'object_id__exact'
    ]

    ordering = ['action_time']

    def action(self, obj):
        return obj.get_change_message()

    def done_by_id(self, obj):
        return obj.user_id

    def done_on_id(self, obj):
        return obj.object_id

    def done_by_username(self, obj):
        if obj.user.first_name:
            return obj.user.first_name
        return None

    def action_flag_(self, obj):
        flags = {
            1: "Addition",
            2: "Changed",
            3: "Deleted",
        }
        return flags[obj.action_flag]


admin.site.register(LogEntry, LogEntry_admin)
