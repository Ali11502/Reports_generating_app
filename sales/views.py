# Django
from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Sale
from .forms import SalesSearchForm
from reports.forms import ReportForm
import pandas as pd
from .utilis import get_chart,get_customer_from_id,get_salesman_from_id
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
@login_required
def home_view(request):
    df1=None
    positions_df=None
    df=None
    merged_df=None
    chart=None
    searchform=SalesSearchForm(request.POST or None )
    reportForm=ReportForm()
    no_data=None
    if request.method=='POST':
        date_from=request.POST.get('date_from')
        date_to=request.POST.get('date_to')
        chart_type=request.POST.get('chart_type')
        results_by = request.POST.get('results_by')

        # print(date_from,date_to,chart_type)
        # qs=Sale.objects.all()
        # print(qs)
        qss=Sale.objects.filter(created__date__gte=date_from,created__date__lte=date_to)
        if len(qss)>0:
            df1=pd.DataFrame(qss.values())
            df1['customer_id']=df1['customer_id'].apply(get_customer_from_id)
            df1['salesman_id']=df1['salesman_id'].apply(get_salesman_from_id)
            df1.rename({'customer_id':'customer','salesman_id':'salesman','id':'sales_id'},axis=1,inplace=True)
            df1['created'] = df1['created'].apply(lambda date: date.strftime('%Y/%m/%d'))
            df1['updated'] = df1['updated'].apply(lambda date: date.strftime('%Y/%m/%d'))
            positions_data = []
            for sale in qss:
                for pos in sale.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sales_id': pos.get_sales_id()
                    }
                    positions_data.append(obj)
            positions_df = pd.DataFrame(positions_data)
            positions_df=positions_df.sort_values(by='sales_id')
            merged_df=pd.merge(df1,positions_df,on='sales_id')
            df=merged_df.groupby('transaction_id',as_index=False)['price'].agg('sum')
            chart=get_chart(chart_type,df1,results_by)
            
            positions_df=positions_df.to_html()
            df1=df1.to_html()
            merged_df=merged_df.to_html()
            df=df.to_html()       
        else:
            no_data='no data available'
        # in values we see column names not in value list
        # print(qss.values())
        # print(qss.values_list())
        # df2=pd.DataFrame(qss.values_list())
        # print(df2)
        # obj=Sale.objects.get(id=2)
        # print(obj)
    context={'search_form':searchform,'sales_list':df1,'positions':positions_df,
             'merged':merged_df,
             'df':df,'chart':chart,
             'report_form':reportForm,
             'no_data':no_data}
    return render(request,"sales/home.html",context)

class SaleListView(LoginRequiredMixin,ListView):
    model=Sale
    template_name='sales/list.html'

class SaleDetailView(LoginRequiredMixin,DetailView):
    model=Sale
    template_name='sales/detail.html'