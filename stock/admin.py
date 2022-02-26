from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models import *
from userprofile.models import Profile



class item_display(admin.ModelAdmin):
    list_display = ('item_name', 'item_configuration', 'item_price', 'item_qty')
    list_filter = ("item_name", "item_configuration")
    search_fields = ['item_name', 'item_configuration']


class item_issue_display(admin.ModelAdmin):

    list_display = ('item_name', 'item_model','acblock', 'inst',  'room', 'item_qty')
    list_filter = ('item_name', 'room')
    search_fields = ['item_name__item_name', 'room']

class item_purchase_display(admin.ModelAdmin):
    list_display = ('item_purchase_date','item_name', 'item_model','item_vendor', 'item_invoice','item_price','item_qty')
    list_filter = ('item_name', 'item_vendor')
    search_fields = ['item_name__item_name', 'item_vendor','item_model']

class LogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drilldown navigation in the admin page
    # date_hierarchy = 'action_time'

    # to filter the resultes by users, content types and action flags
    list_filter = ['user','content_type','action_flag']
    # when searching the user will be able to search in both object_repr and change_message
    search_fields = ['object_repr','change_message' ]        
    list_display = ['action_time','user','content_type','object_repr','action_flag',   ]
        
admin.site.register(ItemName)
admin.site.register(ItemModel)
admin.site.register(ItemDist, item_issue_display)
admin.site.register(RoomType)
admin.site.register(InstituteName)
admin.site.register(ac_block)
admin.site.register(ItemPurchase ,item_purchase_display)
admin.site.register(Profile)
admin.site.register(LogEntry, LogEntryAdmin)

