from django.contrib import admin

from .models import Thread, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 1
    readonly_fields = ('text', 'sender', 'thread', 'created', 'is_read')


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'updated')
    list_display_links = ('id', 'created')
    list_filter = ('created', 'updated')
    search_fields = ('id',)
    readonly_fields = ('id', 'created', 'updated')
    save_on_top = True
    save_as = True
    inlines = [
        MessageInline,
    ]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'thread', 'created', 'is_read')
    list_display_links = ('id', 'created')
    list_filter = ('sender', 'thread', 'is_read')
    search_fields = ('id', 'sender')
    readonly_fields = ('id', 'created')
    save_on_top = True
    save_as = True


admin.site.site_title = 'Simple Chat'
admin.site.site_header = 'Simple Chat'
