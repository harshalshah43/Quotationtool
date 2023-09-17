import django_filters
from .models import *
from django_filters import DateFilter,CharFilter

class PartyFilter(django_filters.FilterSet):
    name = CharFilter(field_name="name",lookup_expr="icontains")
    class Meta:
        model = Party
        fields = ["name"]

class QuotationFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name="date_posted",lookup_expr="gte")
    # end_date = DateFilter(field_name="date_posted",lookup_expr="lte")

    qno = CharFilter(field_name="qno",lookup_expr="icontains")
    enq_ref = CharFilter(field_name="enq_ref",lookup_expr="icontains")
    class Meta:
        model  =Quotation
        fields = "__all__"
        # exclude = ('date_posted')

class QuotationItemsFilter(django_filters.FilterSet):
    item_code = CharFilter(field_name="item_code",lookup_expr="icontains")
    class Meta:
        model = QuotationItems
        fields = ["item_code"]

class ItemFilter(django_filters.FilterSet):
    item_code = CharFilter(field_name="item_code",lookup_expr="icontains")
    item_description = CharFilter(field_name="item_description",lookup_expr="icontains")
    MRP = CharFilter(field_name="MRP",lookup_expr="icontains")
    BP = CharFilter(field_name="BP",lookup_expr="icontains")
    MOQ = CharFilter(field_name="MOQ",lookup_expr="icontains")
    class Meta:
        model = Item
        fields = "__all__"
          