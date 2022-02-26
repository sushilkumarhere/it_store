from . import views
from django.urls import path


urlpatterns = [
    # main Site URLs
    path('cpanel/', views.cpanel, name='cpanel'),
    path('', views.home, name='home'),
    path('system/', views.item_list, name='computer_list'),
    path('excel/', views.export_xls_issue, name='export_xls_issue'),
    path('excel_perchase/', views.export_xls_purchase, name='export_xls_purchase'),  


    # Control Panel Site URLs
    #path('cpanel/', views.cpanel, name='cpanel'),
    
    path('SignOut/', views.signout, name='SignOut'),
    path('cpanel/change-password/', views.change_password, name='change-password'),
    path('cpanel/AdminItems/', views.citem_list, name='item_list'),
    path('cpanel/CreateItemList/', views.create_item_list, name='create_item_list1'),
    path('ajax/load-ItemModel/', views.load_ItemModel, name='ajax_load_ItemModel'),
    path('cpanel/UpdateItemList/<int:item_id>', views.update_item_list, name='update_item_list'),
    path('cpanel/DeleteItem/<int:item_id>',views.delete_item, name='Deleteitem'),
    path('cpanel/approved/<int:item_id>', views.item_approved, name='item_approved'),
    path('cpanel/chart/', views.chart_bar, name='chart_bar'),
    path('cpanel/chart1/', views.chart_bar1, name='chart_bar1'),
    path('cpanel/brandwise/', views.item_brandwise, name='item_brandwise'),
    path('cpanel/itempurchase/', views.itempurchase, name='itempurchase'),
    path('cpanel/itempurchaselist/', views.itempurchaselist, name='itempurchaselist'),
    path('cpanel/currentsttaus/', views.currentsttaus, name='currentsttaus'),
    path('cpanel/PurchaseItemDelete/<int:item_id>',views.purchase_item_delete, name='purchase_item_delete'),
    path('cpanel/PurchaseItemUpdate/<int:item_id>', views.purchase_item_update, name='purchase_item_update'),
    path('cpanel/IssueStatus/', views.IssueStatus, name='IssueStatus'),
    path('cpanel/purchase/Print', views.GeneratePdf_purchase_items.as_view(), name='print_purchase_item'),
    path('cpanel/issue/print/', views.GeneratePdf_issue_items.as_view(), name='print_issue_item'),
    path('cpanel/scrapadd/', views.itemscrap, name='itemscrap'),
    path('cpanel/scraplist/', views.itemscraplist, name='itemscraplist'),
    path('cpanel/ScrapItemUpdate/<int:item_id>', views.itemscrap_update, name='itemscrap_update'),    
    
]   