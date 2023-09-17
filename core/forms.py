from django import forms
from matplotlib import widgets
from .models import *

class DateInput(forms.DateInput):
    input_type='date'

class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        widgets={'date_posted':DateInput()}
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PartyForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = False
        self.fields['email'].required = False
        self.fields['billing_address'].required = False
        self.fields['pincode'].required = False
        


class QuotationForm(forms.ModelForm): # form for any registered party
    class Meta:
        model = Quotation
        widgets={'date_posted':DateInput()}
        exclude = ('total','totalnos','tandc')
        labels = {
            'qno': ('Quotation Number'),
            'enq_ref':('Enquiry Reference Number')
        }
    def __init__(self, *args, **kwargs):
        super(QuotationForm, self).__init__(*args, **kwargs)
        self.fields['qno'].required = False
        self.fields['enq_ref'].required = False
        self.fields['party'].required = False
        self.fields['date_posted'].required = False


class QuotationForm2(forms.ModelForm): # form for a specific party
    class Meta:
        model = Quotation
        widgets={'date_posted':DateInput()}
        exclude = ('author','total','totalnos','tandc','party')
        labels = {
            'qno': ('Quotation Number'),
            'enq_ref':('Enquiry Reference Number')
        }
    def __init__(self, *args, **kwargs):
        super(QuotationForm2, self).__init__(*args, **kwargs)
        self.fields['qno'].required = False
        self.fields['enq_ref'].required = False
        self.fields['date_posted'].required = False


class TandCForm(forms.ModelForm):
    class Meta:
        model = TandC
        exclude = ('quotation',)

class QuotationItemForm(forms.ModelForm):
    class Meta:
        model = QuotationItems
        fields = ["item_code","item_description","discount","margin","price_quoted","qty","sub_total"]
        labels = {
            'discount': ('Discount %'),
            'margin': ('Margin [0.1 to 0.99]')
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["item_code","item_description","MRP","BP","MOQ"]

    def clean_item_code(self):
        item_code_passed =self.cleaned_data.get('item_code')
        if Item.objects.filter(item_code=item_code_passed).exists():
            raise forms.ValidationError(('Item_exists'), code='invalid')
        return item_code_passed

