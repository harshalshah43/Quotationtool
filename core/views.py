from typing import List
from cv2 import log
from django.shortcuts import render,redirect
from django.http.response import HttpResponse,JsonResponse,HttpResponseRedirect
from .models import *
from .forms import *
import csv
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .filters import *

@login_required
def create_party(request):
    form = PartyForm()
    context = {
        'form':form
    }
    if request.method == "POST":
        form = PartyForm(request.POST)
        if form.is_valid():
            form.save()
            party = Party.objects.all().last()
            return redirect('create-quote-for-party',id = party.id)
        else:
            print("Failed ")
            # return render('')
            pass

    return render(request,'core/PartyForm.html',context)

@login_required
def delete_party_confirm(request,id):
    party = Party.objects.get(id=id)
    quotations = Quotation.objects.filter(party = party)
    if party:
        context = {
        'party':party,
        'quotations':quotations,
        'quotation_count':quotations.count()
        }
        return render(request,'core/delete_party_confirm.html',context)
    else:
        return render(request,'error.html')

@login_required
def delete_party(request,id):
    if Party.objects.filter(id=id).exists:
        Party.objects.get(id=id).delete()
        # next = request.POST.get('next', '/')
        # return HttpResponseRedirect(next)
        return redirect('party-master-view')
    else:
        return render(request,'error.html')

def edit_party(request,id):
    party = Party.objects.get(id = id)
    form = PartyForm(instance = party)
    if request.method == "POST":
        form = PartyForm(request.POST,instance = party)
        if form.is_valid():
            form.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        else:
            pass
    else:
        context = {
            'form':form
        }
        return render(request,'core/PartyForm.html',context)

# ------------------------------CRUD Quotations-----------------------------------------------
# @login_required
# def create_quote(request):
#     form = QuotationForm()
#     context = {
#         'form':form,
#     }
#     if request.method == "POST":
#         form = QuotationForm(request.POST)
#         if form.is_valid():
#             quote = form.save(commit=False)
#             quote.save()
#             return redirect('terms-and-conditions',id = quote.id)
#         else:
#             pass
#     return render(request,'core/QuotationForm.html',context)

@login_required
def create_quote_for_party(request,id):
    party = Party.objects.get(id=id)
    q_form = QuotationForm2()
    context = {
        'q_form':q_form,
        'party':party
    }
    if request.method == "POST":
        q_form = QuotationForm2(request.POST or None)
        # t_form = TandCForm(request.POST or None)
        if q_form.is_valid():
            quote = q_form.save(commit = False)
            quote.party = party
            quote.save()
            tandc = TandC.objects.create(quotation = quote)
            tandc.save()
            return redirect('create-quote-items',id = quote.id)
        else:
            return render(request,'core/error.html')
    return render(request,'core/QuotationForm.html',context)

@login_required
def create_party_and_quote(request):
    p_form = PartyForm()
    q_form = QuotationForm2()
    context = {
        'p_form':p_form,
        'q_form':q_form
    }
    if request.method == "POST":
        p_form = PartyForm(request.POST)
        q_form = QuotationForm2(request.POST)
        if p_form.is_valid() and q_form.is_valid():
            p_form.save()
            quote = q_form.save(commit=False)
            party = Party.objects.all().last()
            quote.party = party
            quote.save()
            qid = quote.id
            tandc = TandC.objects.create(quotation = quote)
            tandc.save()
            return redirect('create-quote-items',id = qid)
    return render(request,'core/QuotationForm_copy.html',context)

@login_required
def delete_quote_confirm(request,id):
    quote = Quotation.objects.get(id=id)
    items = QuotationItems.objects.filter(quotation = quote)
    if quote:
        context = {
        'quote':quote,
        'items':items,
        'item_count':items.count()
        }
        return render(request,'core/delete_quote_confirm.html',context)
    else:
        return render(request,'error.html')

@login_required
def delete_quote(request,id):
    if Quotation.objects.filter(id=id).exists:
        Quotation.objects.get(id=id).delete() # TandC object gets deleted as Quotation is deleted.
        TandC.objects.filter()
        return redirect('quotations')
    else:
        return render(request,'error.html')

def edit_quote(request,id):
    quote = Quotation.objects.get(id=id)
    q_form = QuotationForm2(instance=quote)
    if request.method == "POST":
        q_form = QuotationForm2(request.POST,instance=quote)
        if q_form.is_valid():
            q_form.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        else:
            pass
    context = {
        'q_form':q_form,
        'party':quote.party
    }
    return render(request,'core/QuotationForm.html',context)

@login_required       
def terms_and_conditions(request,id):
    quote = Quotation.objects.get(id=id)
    form = TandCForm()
    form.instance.quotation = quote
    context = {
        'form':form,
        'quote':quote
    }
    if request.method =="POST":
        form = TandCForm(request.POST)
        if form.is_valid():
            tandc = form.save(commit = False)
            tandc.quotation = quote
            tandc.save()
            return redirect('create-quote-items',id = quote.id)
        else:
            print("Failed")
            print(form.errors)
    
    return render(request,'core/TandCForm.html',context)

@login_required

def edit_tandc(request,id):
    tandc = TandC.objects.get(id=id)
    qid = tandc.quotation.id
    quote = Quotation.objects.get(id = qid)
    form = TandCForm(instance = tandc)
    if request.method == "POST":
        form = TandCForm(request.POST or None,instance = tandc)
        if form.is_valid():
            tandc = form.save(commit = False)
            tandc.quotation = quote
            tandc.save()
            return redirect('create-quote-items',id = quote.id)
        else:
            print("Failed")
            print(form.errors)
    context = {
        'form':form,
        'quote':quote
    }
    return render(request,'core/TandCForm.html',context)


# ---------------------AutoComplete--------------------
def autocomplete_item_desc(request):
    print(request.GET)
    if 'term' in request.GET:
        qs = QuotationItems.objects.filter(description__icontains = request.GET.get('term'))[:8]
        print(qs)
        items = list()
        for item in qs:
            items.append(item.description)
        return JsonResponse(items,safe = False)

def autocomplete_item_code(request):
    print(request.GET)
    if 'term' in request.GET:
        qs = Item.objects.filter(item_code__icontains = request.GET.get('term'))[:8]
        # qs2 = T2.objects.filter(item_code__icontains = request.GET.get('term'))[:8]
        items = list()
        for item in qs:
            items.append(item.item_code)
        # for item in qs2:
        #     items.append(item.item_code)
        return JsonResponse(items,safe = False)

def auto_fill_get_item_price_quoted(request):
    # print("-------------------------------------------",request.GET['item_code'])
    item_code = request.GET['item_code']
    item = QuotationItems.objects.filter(item_code__icontains = item_code).first()
    if item:
        print("-----------------------------breakpoint1-----------------------")
        context = {'price_quoted':item.price_quoted}
    else:
        print("-----------------------------breakpoint2-----------------------")
        # item = T2.objects.filter(item_code__icontains = item_code).first()
        # context = {'description':item.description,'moq':item.moq,'price':item.lp}
    return JsonResponse(context)

def auto_fill_get_item_mrp(request):
    item_code = request.GET['item_code']
    print("item_code",item_code)
    item = Item.objects.filter(item_code = item_code).first()
    print('MRP',item.MRP)
    print('BP',item.BP)
    context = {'MRP':item.MRP,'BP':item.BP}
    return JsonResponse(context)

#-----------------------------------------CRUD Quotation Items--------------------
def create_quotation_items2(request,id):
    if Quotation.objects.filter(id=id).exists():
        quote = Quotation.objects.get(id = id)
    else:
        return render(request,'core/error.html')
    items = QuotationItems.objects.filter(quotation = quote)
    form = QuotationItemForm(request.POST or None)
    quote.total,quote.totalnos = update_total(items.values())
    # if TandC.objects.filter(quotation= quote).exists():
    #     tandc = TandC.objects.filter(quotation = quote).first()
    # else:
    #     tandc = TandC.objects.create(quotation = quote)
    tandc = TandC.objects.filter(quotation = quote).first()
    context = {
        'form':form,
        'items':items,
        'quote':quote,
        'tandc':tandc,
        'item_count':items.count()
    }
    return render(request,'core/QuotationItemsForm.html',context)
import math
def update_total(items):
    total = 0
    totalnos = 0
    for item in items:
        total+=item['sub_total']
        totalnos+=item['qty']
    total = math.ceil(total)
    return total,totalnos

# def update_item_count(items):
#     item_count = 0
#     for item in items:
#         item_count+=1
#     return item_count

def save_item(request,id):
    if Quotation.objects.filter(id=id).exists():
        quote = Quotation.objects.get(id = id)
    else:
        return render(request,'core/error.html')
    if request.method == "POST":
        form = QuotationItemForm(request.POST or None)
        # print(request.POST['item_code'])
        # print(request.POST)
        if form.is_valid():
            itemid = request.POST.get('itemid')
            # print("itemid",itemid)
            if itemid == '': # if item does not exist,insert it as new item
                item = form.save(commit=False)
                item.quotation = quote
                item.save()
            else: # if item exists then update it with new values passed from the form
                item = QuotationItems.objects.get(id=itemid)
                item.item_code = request.POST['item_code']
                item.discount = request.POST['discount']
                item.margin = request.POST['margin']
                item.price_quoted = request.POST['price_quoted']
                item.qty = request.POST['qty']
                item.sub_total = request.POST['sub_total']
                item.save()
            items = QuotationItems.objects.filter(quotation = quote).values()
            items = list(items)
            quote.total,quote.totalnos = update_total(items)
            quote.save()
            print(items)
            return JsonResponse({'status':'Save','items':items,'total':quote.total,'totalnos':quote.totalnos,'item_count':len(items)})
        else:
            print("Failed")
            print(form.errors)
            return JsonResponse({'status':0})
# warning! this is different type of view function, doesnot take id through formal arguments, but via POST request made through AJAX callback

def delete_item(request):
    if request.method == "POST":
        id = request.POST.get('itemid')
        item = QuotationItems.objects.get(id=id)
        qid = item.quotation.id
        item.delete()
        quote = Quotation.objects.get(id = qid)
        items = QuotationItems.objects.filter(quotation = quote).values()
        quote.total,quote.totalnos = update_total(items)
        quote.save()
        return JsonResponse({'status':1,'total':quote.total})
    else:
        return JsonResponse({'status':0})

def edit_item(request):
    if request.method == "POST":
        id = request.POST.get('itemid')
        item = QuotationItems.objects.get(id=id)
        item_data = {"itemid":item.id,"item_code":item.item_code,"discount":item.discount,"margin":item.margin,"price_quoted":item.price_quoted,'qty':item.qty,'sub_total':item.sub_total}
        qid = item.quotation.id
        quote = Quotation.objects.get(id = qid)
        items = QuotationItems.objects.filter(quotation = quote).values()
        quote.total,quote.totalnos = update_total(items)
        quote.save()
        return JsonResponse(item_data)

@login_required
def download_quote(request,id):
    quoteid = id
    quote = Quotation.objects.filter(id = quoteid).first()
    # items = Item.objects.filter(rt = rt)
    # context = {
    #     'items':items,
    #     'rt':rt
    # }

    response = HttpResponse(content_type = "text/csv")
    writer = csv.writer(response)
    writer.writerow(["Quotation Details"])
    writer.writerow(["Party: "+quote.party.name])
    writer.writerow(["Date Posted: "+str(quote.date_posted)])
    writer.writerow(["Total: "+str(quote.total)])
    writer.writerow([])
    writer.writerow(['Item Code','Price Quoted','Qty','Sub Total'])
    for item in QuotationItems.objects.filter(quotation = quote).values_list('item_code','price_quoted','qty','sub_total'):
        writer.writerow(item)
    response['Content-Disposition'] = f'attachment; filename = "{quote.party} dated:{quote.date_posted}.csv"'
    return response

def view_printable_version(request,id):
    quote = Quotation.objects.get(id=id)
    tandc = TandC.objects.get(quotation = quote)
    items = QuotationItems.objects.filter(quotation = quote)
    items_list = []
    for item in items:
        items_dict = dict()
        items_dict['item'] = item
        items_dict['item_description'] = Item.objects.filter(item_code__icontains = item.item_code).first().item_description
        items_list.append(items_dict)
    if quote:
        gst_18 = math.ceil(quote.total * 0.18)
        total_gst = gst_18 + quote.total
        context = {
        'quote':quote,
        'tandc':tandc,
        'items_list':items_list,
        'item_count':items.count(),
        'gst_18':gst_18,
        'total_gst':total_gst
        }
        return render(request,'core/print_quotation.html',context)
    else:
        return render(request,'error.html')

from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import View

@login_required
def render_to_pdf(template_src,context_dict = {}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode(encoding = 'UTF-8')),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type = 'application/pdf')
    return None

@login_required
def ViewPDF(request,id):
    # def get(self,request,*args,**kwargs):
    quote = Quotation.objects.get(id=id)
    items = QuotationItems.objects.filter(quotation = quote)
    if quote:
        context = {
        'quote':quote,
        'items':items,
        'item_count':items.count()
        }
    pdf = render_to_pdf('core/print_quotation.html',context)
    return HttpResponse(pdf,content_type = 'application/pdf')

# ------------------------------VIEWS----------------------------------------------
# class QuotationListView(ListView):
#     model = Quotation
#     template_name = "core/quotations.html" 
#     context_object_name='quotations'

@login_required 
def PartyMasterView(request): # Party CRUD operations
    parties = Party.objects.all()
    context = {
        'parties':parties
    }
    return render(request,'core/PartyMasterView.html',context)


@login_required
def PartyListView(request):
    parties = Party.objects.all()
    context = {
        'parties':parties
    }
    return render(request,'core/PartyView.html',context)

@login_required
def QuotationListView(request):
    quotations = Quotation.objects.all().order_by('-date_posted')
    myfilter = QuotationFilter(request.GET,queryset=quotations)
    quotations = myfilter.qs
    context = {
        'quotations':quotations,
        'myfilter':myfilter
    }
    return render(request,'core/quotations.html',context)

@login_required
def QuotationsListViewPartyWise(request,id):
    party = Party.objects.get(id=id)
    quotations = Quotation.objects.filter(party = party).order_by('-date_posted')
    myfilter = QuotationFilter(request.GET,queryset=quotations)
    quotations = myfilter.qs
    context = {
        'quotations':quotations,
        'party':party,
        'myfilter':myfilter
    }
    return render(request,'core/quotations_for_party.html',context)
    
# class PartyListView(ListView):
#     model = Party
#     template_name = ""

@login_required
def QuotationItemsView(request):
    quotationitems = QuotationItems.objects.all()
    myfilter = QuotationItemsFilter(request.GET,queryset=quotationitems)
    quotationitems = myfilter.qs
    context = {
        'quotationitems':quotationitems,
        'myfilter':myfilter
    }
    return render(request,'core/QuotationItems.html',context)

@login_required
def quoteitems_for_item_code(request,id):
    item_code = QuotationItems.objects.filter(id=id).first().item_code
    quotationsitems = QuotationItems.objects.filter(item_code=item_code)
    context = {
        'quotationitems':quotationsitems
    }
    return render(request,'core/QuotationItems.html',context)

@login_required
def quoteitems_for_party(request,id):
    party = QuotationItems.objects.filter(id=id).first().quotation.party
    quotations = Quotation.objects.filter(party = party)
    quotationitems = QuotationItems.objects.none()
    for quote in quotations:
        quotationitems=quotationitems.union(QuotationItems.objects.filter(quotation = quote))
    # quotationitems = QuotationItems.objects.filter(quotation=party)
    print("quotationitems",quotationitems)
    context = {
        'quotationitems':quotationitems
    }
    return render(request,'core/QuotationItems.html',context)

@login_required
def back(request):
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)  

#-----------------------------------------CRUD Items--------------------

@login_required
def create_item_master(request):
    form = ItemForm(request.POST or None)
    context = {
        'form':form
    }
    return render(request,'core/itemform.html',context)

# cannot use the same logic as save-item because of uniqueness constraint in models.py
def save_item_master(request):
    if request.method == "POST":
        itemid = request.POST.get('itemid')
        print('itemid', itemid)
        context = {}
        if itemid == '':
            form = ItemForm(request.POST)
            if form.is_valid():
                form.save()
                context['error'] = "None"
                context['status'] = "saved"
            else:
                context['error'] = "form is not valid"
                context['status'] = 0
        else:
            item = Item.objects.get(id=itemid)
            item.item_code = request.POST['item_code']
            item.item_description = request.POST['item_description']
            item.MRP = request.POST['MRP']
            item.save()
            context['error'] = "None"
            context['status'] = "saved"
        items = Item.objects.all().values()
        items = list(items)
        context['items'] = items
        return JsonResponse(context)
            

@login_required
def ItemMasterView(request):
    items = Item.objects.all()
    form = ItemForm(request.POST or None)
    myfilter = ItemFilter(request.GET,queryset=items)
    items = myfilter.qs
    context = {
        'items':items,
        'form':form,
        'myfilter':myfilter
    }
    return render(request,'core/ItemMasterView.html',context)

def delete_item_master(request):
    if request.method == "POST":
        id = request.POST.get('itemid')
        print(id)
        item = Item.objects.get(id=id)
        item.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})

def edit_item_master(request):
    if request.method == "POST":
        id = request.POST.get('itemid')
        print(id)
        item = Item.objects.get(id=id)
        item_data = {"itemid":id,"item_code":item.item_code,"item_description":item.item_description,"MRP":item.MRP}
        return JsonResponse(item_data)
    else:
        return JsonResponse({'status':0})

# ----------------------------------------------FILTERS----------------------------------------------------
