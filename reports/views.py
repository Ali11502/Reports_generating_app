from django.shortcuts import render,get_object_or_404
from profiles.models import Profile
from django.http import JsonResponse
from .utilis import get_report_image
from .models import Report
from django.views.generic import ListView,DetailView,TemplateView
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from sales.models import Sale,Position,CSV
from django.utils.dateparse import parse_date
from products.models import Products
from customers.models import Customer
import requests
import csv
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class ReportListView(LoginRequiredMixin,ListView):
    model=Report
    template_name='reports/list.html'

class ReportDetailView(LoginRequiredMixin,DetailView):
    model=Report
    template_name='reports/detail.html'

class UploadTemplateView(LoginRequiredMixin,TemplateView):
    template_name='reports/from_file.html'
@login_required
def csv_upload_view(request):
    if request.method == 'POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        
        _,created=CSV.objects.get_or_create(file_name=csv_file_name)
        if created:
            csv_file.save()
        # Ensure the file is read correctly from memory
            csv_file.seek(0)  # Move to the beginning of the file
            reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
            reader.__next__()
            for row in reader:
                transaction_id = row[1]
                product = row[2]
                quantity = int(row[3])
                customer = row[4]
                date = parse_date_custom(row[5])
                
                try:
                    product_obj = Products.objects.get(name__iexact=product)
                except Products.DoesNotExist:
                    product_obj = None
                
                if product_obj is not None:
                    customer_obj, _ = Customer.objects.get_or_create(name=customer)
                    salesman_obj = Profile.objects.get(user=request.user)
                    position_obj = Position.objects.create(product=product_obj, quantity=quantity, created=date)

                    sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id,
                            customer=customer_obj, salesman=salesman_obj, created=date)
                    sale_obj.positions.add(position_obj)
                    # sale_obj.save()
            return JsonResponse({'ex':False})
        else:
            return JsonResponse({'ex':True})

    return HttpResponse()
from datetime import datetime

def parse_date_custom(date_string):
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        return None
    
@login_required
def create_report_view(request):
    print('in create report view')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        image = request.POST.get('image')
        img=get_report_image(image)
        author = Profile.objects.get(user=request.user)
        Report.objects.create(name=name, remarks=remarks, image=img, author=author)

        return JsonResponse({'message': 'Report created successfully'})

    return JsonResponse({'message': 'outside if'})

@login_required
def render_pdf_view(request,pk):
    template_path = 'reports/pdf.html'
    obj = get_object_or_404(Report, pk=pk)
    context = {'obj': obj}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
#    for downloading
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
  
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
