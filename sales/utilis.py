import uuid,base64
from io import BytesIO
import matplotlib.pyplot as plt
from customers.models import Customer
from profiles.models import Profile
import seaborn as sns
def generate_code():
    code=str(uuid.uuid4()).replace('-','')[:12]
    return code
def get_salesman_from_id(val):
    salesman = Profile.objects.get(id=val)
    return salesman.user.username

def get_customer_from_id(val):
    customer = Customer.objects.get(id=val)
    return customer

def get_graph():
    # Create an in-memory binary stream
    buffer = BytesIO()
    
    # Save the current figure to the buffer as a PNG image
    plt.savefig(buffer, format='png')
    
    # Move the file pointer to the beginning of the buffer
    buffer.seek(0)
    
    # Read the contents of the buffer (the PNG image) into a bytes object
    image_png = buffer.getvalue()
    
    # Encode the bytes object into a base64 encoded bytes object
    graph = base64.b64encode(image_png)
    
    # Decode the base64 encoded bytes object into a string
    graph = graph.decode('utf-8')
    
    # Close the buffer to free up resources
    buffer.close()
    
    # Return the base64 encoded string of the PNG image
    return graph

def get_key(resby):
    key=None
    if resby=='#1':
        key='transaction_id'
    elif resby=='#2':
        key='created'
    return key


def get_chart(chart_type,data,results_by,**kwargs):
    plt.switch_backend('AGG')
    fig=plt.figure(figsize=(10,4))
    key=get_key(results_by)
    d=data.groupby(key,as_index=False)['total_price'].agg('sum')
    if chart_type=='#1':
        # plt.bar(data['transaction_id'],data['price'])
        # plt.xlabel('Transaction ID')
        # plt.ylabel('Price')
        sns.barplot(x=key, y='total_price', data=d)

    elif chart_type=='#2':
        plt.pie(data=d,x='total_price',labels=d[key].values)
        

    elif chart_type=='#3':
        plt.plot(d[key],d['total_price'])
        plt.xlabel(key)
        plt.ylabel('total_price')
    else:
        print('failed to idetify the chart type')
    plt.tight_layout()
    chart=get_graph()
    return chart