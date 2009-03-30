from django.contrib import admin
from models import Item, Collection


class ItemAdmin(admin.ModelAdmin):
    list_filter = ('collection',)


admin.site.register(Item, ItemAdmin)
admin.site.register(Collection)
