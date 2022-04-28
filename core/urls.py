from unicodedata import name
from django.urls import path
from .views import *

urlpatterns = [
    
    #CRUD parties
    path('create-party/',create_party,name = "create-party"),
    path('delete-party-confirm/<int:id>/',delete_party_confirm,name = "delete-party-confirm"),
    path('delete-party/<int:id>/',delete_party,name = "delete-party"),
    path('edit-party/<int:id>/',edit_party,name = "edit-party"),

    # path('quote-items/<int:id>/',create_quotation_items,name = 'create-quote-items'),

    # CRUD items
    path('quote-items/<int:id>/',create_quotation_items2,name = 'create-quote-items'),
    path('save-item/<int:id>/',save_item,name = 'save-item'),
    path('delete-item/',delete_item,name = 'delete-item'),
    path('edit-item/',edit_item,name = 'edit-item'),
    path('download_quote_csv/<int:id>/',download_quote,name = 'download-quote-csv'),
    path('view_printable_version/<int:id>/',view_printable_version,name = 'view-printable-version-pdf'),
    path('view-pdf/<int:id>/',ViewPDF,name = 'view-pdf'),
    # path('quote-items-form/',create_quotation_items_form,name = 'create-quote-items-form'),
    # path('item-update/<int:id>/',item_update,name= 'item-update'),
    # path('item-detail/<int:id>/',item_detail,name = 'item-detail'),
    # path('item-delete/<int:id>/',item_delete,name= 'item-delete'),

    path('item-form/autocomplete_code/',autocomplete_item_code,name = 'autocomplete_code'),
    path('item-form/auto_fill_get_item_price/',auto_fill_get_item_price_quoted,name = 'auto_fill_get_item_price'),
    path('item-form/auto_fill_get_item_mrp/',auto_fill_get_item_mrp,name = 'auto_fill_get_item_mrp'),

    # CRUD Item MASTER
    path('create-item-master/',create_item_master,name = 'create-item-master'),
    path('save-item-master/',save_item_master,name = 'save-item-master'),
    path('item-master-view/',ItemMasterView,name = 'item-master-view'),
    path('item-master-delete/',delete_item_master,name = 'item-master-delete'),
    path('item-master-edit/',edit_item_master,name = 'item-master-edit'),

    # CRUD quotations
    # path('quote/',create_quote,name = "create-quote"),
    path('quote/<int:id>/',create_quote_for_party,name = 'create-quote-for-party'),
    path('delete-quote/<int:id>/',delete_quote,name = "delete-quote"),
    path('edit-quote/<int:id>/',edit_quote,name = "edit-quote"),
    path('delete-quote-confirm/<int:id>/',delete_quote_confirm,name = "delete-quote-confirm"),
    path('create-party-quote/',create_party_and_quote,name = 'create-party-and-quote'),
    
    path('terms-and-conditions/<int:id>/',terms_and_conditions,name = 'terms-and-conditions'),
    path('terms-and-conditions-edit/<int:id>/',edit_tandc,name = "edit-tandc"),
    
    #views
    path('quotations/',QuotationListView,name = "quotations"),
    path('quotations-for-party/<int:id>/',QuotationsListViewPartyWise,name = 'quote-for-party'),
    path('',PartyListView,name = 'parties'),
    path('party-master/',PartyMasterView,name = 'party-master-view'),
    path('quotation-items/',QuotationItemsView,name = 'quote-items'),
    path('quotationitems-for-item-code/<int:id>/',quoteitems_for_item_code,name = 'quote-items-for-item-code'),
    path('quotationitems-for-party/<int:id>/',quoteitems_for_party,name = 'quote-items-for-party'),
    #utilities
    path('back/',back,name = 'back')
    
]