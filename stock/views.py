import xlwt,json
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from stock.forms import Create_ItmDist_Form, item_list_update , Item_purchase_create_Form, \
purchase_item_update_form ,Create_scrap_Form ,scrap_update_form
from stock.models import ItemDist, ItemName, ItemModel, ac_block,ItemPurchase , ItemScrap
from django.db.models import Sum, Q , F , Sum    
from django.shortcuts import render, get_object_or_404, redirect
from .filters import Item_dstFilter,Item_PurchaseFilter ,Item_ScrapFilter
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from userprofile.models import Profile
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from stock.utils import render_to_pdf       #created in Utils.py


items_d = ""  # Global Variable for Excel Distrubute Items
items_p = ""  # Global Variable for Excel Purchase Items
items_s = ""  # Global Variable for Excel Scarp Items


# Create your views here.

# Front Views-- Home Page

def home(request):
    comp = ItemDist.objects.all().filter(item_name=1, act=1).aggregate(Sum('item_qty'))
    printer = ItemDist.objects.all().filter(item_name=2, act=1).aggregate(Sum('item_qty'))
    proj = ItemDist.objects.all().filter(item_name=3, act=1).aggregate(Sum('item_qty'))
    scan = ItemDist.objects.all().filter(item_name=4, act=1).aggregate(Sum('item_qty'))
    up = ItemDist.objects.all().filter(item_name=8, act=1).aggregate(Sum('item_qty'))
    updated_on = ItemDist.objects.latest('updated_at')
    choices = {'computer': comp, 'printer': printer, 'projector': proj, 'scanner': scan, 'ups': up,'updt':updated_on}
    return render(request, 'home.html', choices)
    

# Front Views-- List of Issue Items

def item_list(request):
    item_lst = ItemDist.objects.all().filter(act=1).order_by('acblock', 'room','room_type','inst','user','item_name')
    z = request.GET
    item_filter = Item_dstFilter(z, queryset=item_lst)
    global items_d
    items_d = z
    item_qty = item_filter.qs.aggregate(Sum('item_qty'))
    choices = {'filter': item_filter, 'totality': item_qty}
    return render(request, 'item_list.html', choices)

# Front Views-- Export To Excel List

def export_xls_issue(request):
    # call global variable item1
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="item.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('items_d')       # item_d Global Variable for Excel Distrubute Items
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['item Name', 'Model', 'Block', 'Room', 'Room Type', 'Deptartment','user', 'Quantity', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining row
    font_style = xlwt.XFStyle()
    item_lst = ItemDist.objects.all().filter(act=1).order_by('acblock', 'room')
    item_filter = Item_dstFilter(items_d, queryset=item_lst)
    aa = item_filter.qs
    rows = aa.values_list('item_name__item_name', 'item_model__model_name', 'acblock__name', 'room',
                          'room_type__room_type', 'inst__Inst_name','user', 'item_qty')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


def export_xls_purchase(request):
    # call global variable item1
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="item.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('items_p')    # item_p Global Variable for Excel Purchase Items
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Purchase Date','item Name', 'Model', 'Vendor', 'Invoice', 'Price', 'Quantity', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining row
    font_style = xlwt.XFStyle()
    Pitem_lst = ItemPurchase.objects.all().order_by('item_purchase_date', 'item_name')
    item_filter = Item_PurchaseFilter(items_p, queryset=Pitem_lst)
    aa = item_filter.qs
    rows = aa.values_list('item_purchase_date','item_name__item_name', 'item_model__model_name', 'item_vendor', 'item_invoice',
                          'item_price', 'item_qty')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

# Cpanel  Views-- DashBoard C Panel

@login_required
def cpanel(request):
    if not request.user.has_perm('auth.add_group'):
        return render(request, 'cpanel/error.html')
    else:     
        comp = ItemDist.objects.all().filter(item_name=1, act=1).aggregate(Sum('item_qty'))
        printer = ItemDist.objects.all().filter(item_name=2, act=1).aggregate(Sum('item_qty'))
        proj = ItemDist.objects.all().filter(item_name=3, act=1).aggregate(Sum('item_qty'))
        scan = ItemDist.objects.all().filter(item_name=4, act=1).aggregate(Sum('item_qty'))
        up = ItemDist.objects.all().filter(item_name=8, act=1).aggregate(Sum('item_qty'))
        updated_on = ItemDist.objects.latest('updated_at')
        choices = {'computer': comp, 'printer': printer, 'projector': proj, 'scanner': scan, 'ups': up,'updt':updated_on}
         
        return render(request, 'cpanel/AdminHome.html',choices)


# Sign out/Logout  View #
def signout(request):
    logout(request)
    return redirect('home')


# Cpanel  Views-- List of Items
@login_required
def citem_list(request):
    if not request.user.has_perm('auth.view_group'):
        return render(request, 'cpanel/error.html')
    else:      
        item_lst = ItemDist.objects.all().order_by('act', 'acblock', 'room','room_type','inst','user','item_name')
        z = request.GET
        item_filter = Item_dstFilter(z, queryset=item_lst)
        global items_d
        items_d = z        
        item_qty = item_filter.qs.aggregate(Sum('item_qty'))
        choices = {'filter': item_filter, 'totality': item_qty}
    return render(request, 'cpanel/issue/item_list.html', choices)

# Cpanel  Views-- Update Item List
@login_required
def update_item_list(request, item_id, template_name='cpanel/issue/upadate_item_list.html'):
    if not request.user.has_perm('auth.change_group'):
        return render(request, 'cpanel/error.html')
    else:
        post = get_object_or_404(ItemDist, pk=item_id)  # ItemDist is a  Model
        form = item_list_update(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    return render(request, template_name, {'form': form})

# Cpanel  Views-- Delete Item List

@login_required
def delete_item(request, item_id):
    if not request.user.has_perm('auth.delete_group'):
        return render(request, 'cpanel/error.html')
    else:
        obj = get_object_or_404(ItemDist, id=item_id)
        context = {'items': obj}
        if request.method == "POST":
            # delete object
            obj.delete()
            return redirect("item_list")
    return render(request, "cpanel/issue/Delete_items.html", context)

# Cpanel  Views-- Approved Item List

@login_required
def item_approved(request, item_id):
    if not request.user.has_perm('auth.change_group'):
        return render(request, 'cpanel/error.html')
    else:
        obj = get_object_or_404(ItemDist, id=item_id)
        obj.act = 1
        obj.save()
        return redirect("item_list")

# Cpanel  Views-- Add  Issue Item 
@login_required
def create_item_list(request):
    if not request.user.has_perm('auth.add_group'):
        return render(request, 'cpanel/error.html')
    else:
        upload = Create_ItmDist_Form()  # Create_ItmDist_Form is a form
        if request.method == 'POST':
            upload = Create_ItmDist_Form(request.POST, request.FILES)
            if upload.is_valid():
                upload.save()
                messages.success(request, "Item Added successful.")
                return redirect('create_item_list1')
            else:
                messages.error(request, "Item Unsuccessful")
        return render(request, 'cpanel/issue/Create_ItemDist.html', {'upload_form': upload})

# Cpanel  Views-- Status of  Issue Item 
   
@login_required
def IssueStatus(request):
    if not request.user.has_perm('auth.add_group'):
        return render(request, 'cpanel/error.html')
    else:
        queryset1 = ItemDist.objects.values('item_name__item_name').filter(act=1).annotate(
        total_qty_c=Sum('item_qty')).order_by('item_name__item_name')
    queryset = ItemDist.objects.values('acblock__name').annotate(
        total_qty_c=Sum('item_qty', filter=Q(item_name=1, act=1)),
        total_qty_p=Sum('item_qty', filter=Q(item_name=2, act=1)),
        total_qty_pro=Sum('item_qty', filter=Q(item_name=3, act=1)),
        total_qty_s=Sum('item_qty', filter=Q(item_name=4, act=1))) \
        .order_by('acblock')
    choices = {'dataset': queryset, 'ds1': queryset1}
    return render(request, 'cpanel/issue/issue_status.html', choices)

# Cpanel  Views-- Ajax of Load Item Model with respect to Item Name

def load_ItemModel(request):
    item_name_id = request.GET.get('item_name')
    item_model = ItemModel.objects.filter(item_name_id=item_name_id).order_by('model_name')
    return render(request, 'cpanel/modelname_dropdown.html', {'model': item_model})

# Cpanel  Views-- Chart1 of Computers
@login_required
def chart_bar(request):
    labels = []
    data = []
    queryset = ItemDist.objects.values('acblock__name').filter(item_name=1, act=1).annotate(total_qty=Sum('item_qty')) \
        .order_by('acblock')
    for entry in queryset:
        labels.append(entry['acblock__name'])
        data.append(entry['total_qty'])
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

# Cpanel  Views-- Chart of All Items
@login_required
def chart_bar1(request):
    queryset = ItemDist.objects.values('acblock__name').annotate(
        total_qty_c=Sum('item_qty', filter=Q(item_name=1, act=1)),
        total_qty_p=Sum('item_qty', filter=Q(item_name=2, act=1)),
        total_qty_pro=Sum('item_qty', filter=Q(item_name=3, act=1)),
        total_qty_s=Sum('item_qty', filter=Q(item_name=4, act=1))) \
        .order_by('acblock')
    blocks = list()
    computer = list()
    printer = list()
    projector = list()
    scanner = list()
    for entry in queryset:
        blocks.append(entry['acblock__name'])
        computer.append(entry['total_qty_c'])
        printer.append(entry['total_qty_p'])
        projector.append(entry['total_qty_pro'])
        scanner.append(entry['total_qty_s'])
    choices = {'blocks': json.dumps(blocks),
               'computer': json.dumps(computer),
               'printer': json.dumps(printer),
               'projector': json.dumps(projector),
               'scanner': json.dumps(scanner)}
    return render(request, 'cpanel/issue/chart_bar.html', choices)
# Cpanel  Views-- New User Add


# Cpanel  Views-- Change Password of Current User 

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password has been successfully updated!')
            return render(request, 'cpanel/massage.html')            
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'cpanel/user/ChangePass.html', {'form': form })
    

# Cpanel  Views-- List of Items Brand Wise
@login_required
def item_brandwise(request):
    if not request.user.has_perm('auth.view_group'):
        return render(request, 'cpanel/error.html')
    else:
        Pitem_lst = ItemDist.objects.values('item_model__model_name').annotate(
                total_qty_c=Sum('item_qty')).order_by('item_model__model_name')
        z = request.GET        
        bitem_filter = Item_dstFilter(z, queryset=Pitem_lst)    
        item_qty = bitem_filter.qs.aggregate(Sum('total_qty_c'))
        print(item_qty)
        choices = {'filter': bitem_filter,'itmqty':item_qty}                 
        return render(request, 'cpanel/issue/item_brandwise.html', choices)
# Cpanel  Views-- Current Status of Purchase And Issue Items

@login_required
def currentsttaus(request):
    if not request.user.has_perm('auth.add_group'):
        return render(request, 'cpanel/error.html')
    else:     
        purchage_itm=ItemName.objects.values('item_name') \
            .annotate(purchase_qty=Sum('itempurchase__item_qty'))        

        issue_itm = ItemName.objects.values('item_name') \
            .annotate(issue_qty=Sum('itemdist__item_qty'))
        
        scrape_itm = ItemName.objects.values('item_name') \
            .annotate(scrap_qty=Sum('itemscrap__item_qty'))       
                
        choices = {'ds':purchage_itm ,'ds1': issue_itm , 'ds2': scrape_itm}    
        return render(request, 'cpanel/current/current_status.html',choices)

# Cpanel  Views-- Add Purchase Items
@login_required
def itempurchase(request):
    if not request.user.has_perm('auth.delete_group'):
        return render(request, 'cpanel/error.html')
    else:
        upload = Item_purchase_create_Form()  # Create_ItmDist_Form is a form
        if request.method == 'POST':
            upload = Item_purchase_create_Form(request.POST, request.FILES)
            if upload.is_valid():
                upload.save()
                messages.success(request, "Item Added successful.")
                return redirect('itempurchase')
            else:
                messages.error(request, "Item Unsuccessful")
        return render(request, 'cpanel/purchase/item_purchase_create.html', {'upload_form': upload})

# Cpanel  Views-- List Purchase Items

@login_required
def itempurchaselist(request):
    if not request.user.has_perm('auth.add_group'):
        return render(request, 'cpanel/error.html')
    else:
        Pitem_lst = ItemPurchase.objects.all().order_by('item_purchase_date', 'item_name')
        z = request.GET
        Pitem_filter = Item_PurchaseFilter(z, queryset=Pitem_lst)
        global items_p        #  global Variabal for Excel Export
        items_p = z           # Asign z to items
        item_qty = Pitem_filter.qs.aggregate(Sum('item_qty'))
        choices = {'filter': Pitem_filter, 'totality': item_qty}
        return render(request, 'cpanel/purchase/item_purchase_list.html',choices)   
        
# Cpanel  Views-- Delete Purchase Items

@login_required
def purchase_item_delete(request, item_id):
    if not request.user.has_perm('auth.delete_group'):
        return render(request, 'cpanel/error.html')
    else:
        obj = get_object_or_404(ItemPurchase, id=item_id)
        context = {'items': obj}
        if request.method == "POST":
            # delete object
            obj.delete()
            return redirect("itempurchaselist")
    return render(request, "cpanel/issue/Delete_items.html", context)

# Cpanel  Views-- Update Purchase Items

@login_required
def purchase_item_update(request, item_id, template_name='cpanel/purchase/item_purchase_update.html'):
    if not request.user.has_perm('auth.change_group'):
        return render(request, 'cpanel/error.html')
    else:
        post = get_object_or_404(ItemPurchase, pk=item_id)  # ItemPurchase is a  Model
        form = purchase_item_update_form(request.POST or None,request.FILES or None, instance=post)  # purchase_item_update_form is a  Form
        if form.is_valid():
            obj=form.save(commit=False)
            obj.save()
            return redirect('itempurchaselist')
    return render(request, template_name, {'form': form})

class GeneratePdf_purchase_items(View):
     def get(self, request, *args, **kwargs):
        template = get_template('cpanel/purchase/item_purchase_list_pdf.html')
        Pitem_lst = ItemPurchase.objects.all().order_by('item_purchase_date', 'item_name')      
        Pitem_filter = Item_PurchaseFilter(items_p, queryset=Pitem_lst)
        # items_p is the global Variabal from Purchase Item List to Wxport PDF                           
        choices = {'filter': Pitem_filter}
        #html = template.render(choices)
        pdf = render_to_pdf('cpanel/purchase/item_purchase_list_pdf.html', choices)
        #return HttpResponse(pdf, content_type='application/pdf')
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "PurchaseItemList%s.pdf" %("001")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

class GeneratePdf_issue_items(View):
     def get(self, request, *args, **kwargs):
        template = get_template('cpanel/issue/item_issue_list_pdf.html')
        issue_item_lst = ItemDist.objects.all().order_by('act', 'acblock', 'room','room_type','inst','user','item_name')
        Ditem_filter = Item_dstFilter(items_d, queryset=issue_item_lst)
        # items_d is the global Variabal from issue/Distrubution Item List to Wxport PDF                           
        choices = {'filter': Ditem_filter}
        #html = template.render(choices)
        pdf = render_to_pdf('cpanel/issue/item_issue_list_pdf.html', choices)
        #return HttpResponse(pdf, content_type='application/pdf')
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "IssueItemList%s.pdf" %("001")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

# Scrap Item View
@login_required
def itemscrap(request):
    if not request.user.has_perm('auth.add_group'):
        return render(request, 'cpanel/error.html')
    else:
        upload = Create_scrap_Form()  # Create_scrap_Form is a form
        if request.method == 'POST':
            upload = Create_scrap_Form(request.POST, request.FILES)
            if upload.is_valid():
                upload.save()
                messages.success(request, "Item Added successful.")
                return redirect('itemscrap')
            else:
                messages.error(request, "Item Unsuccessful")
        
    return render(request, "cpanel/scrap/itemscrap.html",{'upload_form': upload})
#   Views-- List of Scrap Items
@login_required
def itemscraplist(request):
    if not request.user.has_perm('auth.view_group'):
        return render(request, 'cpanel/error.html')
    else:      
        item_lst = ItemScrap.objects.all().order_by('item_name')
        z = request.GET
        item_filter = Item_ScrapFilter(z, queryset=item_lst)
        global items_d
        items_s = z
        
        item_qty = item_filter.qs.aggregate(Sum('item_qty'))
        choices = {'filter': item_filter, 'totality': item_qty}
    return render(request, 'cpanel/scrap/itemscrap_list.html', choices)

@login_required
def itemscrap_update(request, item_id, template_name='cpanel/scrap/itemscrap_update.html'):
    if not request.user.has_perm('auth.change_group'):
        return render(request, 'cpanel/error.html')
    else:
        post = get_object_or_404(ItemScrap, pk=item_id)  # ItemPurchase is a  Model
        form = scrap_update_form(request.POST or None,request.FILES or None, instance=post)  # purchase_item_update_form is a  Form
        if form.is_valid():
            obj=form.save(commit=False)
            obj.save()
            return redirect('itemscraplist')
    return render(request, template_name, {'form': form})
