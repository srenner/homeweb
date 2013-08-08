from django.http import HttpResponse
from HomeWeb.billminder.models import Bill, BillPayment #@UnresolvedImport
from django.shortcuts import get_object_or_404, render_to_response
from django.core import serializers
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
#import datetime
#from django.utils import simplejson
## Django 1.5+ compat
try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.db import connection
import datetime
from django.db import backend
from django.db.models.aggregates import Max

@login_required
def index(request):
    bills = Bill.objects.filter(is_active=True)
    force_json = False
    if 'format' in request.GET:
        if request.GET['format'].lower() == 'json':
            force_json = True
    if request.is_ajax() or force_json:
        mimetype = "application/json"
        outputFormat = "json"
        data = serializers.serialize(outputFormat, bills, extras=('health','days_since_payment'))
        return HttpResponse(data, mimetype)
    else:
        return render_to_response("BillMinder/index.html", {'bills': bills}, context_instance=RequestContext(request))
    

@login_required
def detail(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)
    pass
    if request.is_ajax():
        mimetype = "application/json"
        outputFormat = "json"
        data = serializers.serialize(outputFormat, [bill])
        return HttpResponse(data, mimetype)
    else:
        return render_to_response("BillMinder/detail.html", {'bill': bill}, context_instance=RequestContext(request))
        
def logout_view(request):
    return logout_then_login(request)

@login_required    
def make_payment(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)
    #YYYY-MM-DD HH:MM[:ss[.uuuuuu]]
    #02/29/2012 15:32
    raw_dt = request.POST['payment_date']
    formatted_payment_date = raw_dt[6:10] + '-' + raw_dt[0:2] + '-' + raw_dt[3:5] + ' ' + raw_dt[11:]
    if not bill.last_payment_date or formatted_payment_date > str(bill.last_payment_date):
        bill.last_payment_date = formatted_payment_date
        bill.default_amount = request.POST['amount']
        bill.default_reminder_days = request.POST['reminder_days']    
    bill.save()
    
    payment = BillPayment(bill=bill, 
                          payment_date=formatted_payment_date,
                          payment_amount=request.POST['amount'],
                          reminder_days=request.POST['reminder_days'],
                          confirmation_number=request.POST['confirmation_number'],
                          notes=request.POST['notes'])
    payment.save()
    return HttpResponse(bill_id)

@login_required
def get_payments(request, bill_id):
    if 'count' in request.GET:
        #clumsy reverse ordering + reverse() call because Django does not support python's negative indexing
        payments = list(BillPayment.objects.filter(bill=bill_id).order_by('-payment_date')[0:request.GET['count']])
        payments.reverse()
    else:
        payments = list(BillPayment.objects.filter(bill=bill_id).order_by('payment_date'))
    mimetype = "application/json"
    outputFormat = "json"
    data = serializers.serialize(outputFormat, payments)
    return HttpResponse(data, mimetype)

@login_required
def get_alerts(request, only_new, process):
    force_json = False
    if 'format' in request.GET:
        if request.GET['format'].lower() == 'json':
            force_json = True
    

    where_email_clause = ""
    if only_new == True:
        where_email_clause = "and bp.reminder_email_sent = 0"
    billpayments = BillPayment.objects.raw("select bp.* from billminder_bill b inner join billminder_billpayment bp on b.id = bp.bill_id " + 
    "left outer join billminder_billpayment bp2 on bp.bill_id = bp2.bill_id and bp.payment_date < bp2.payment_date " + 
    "where bp2.payment_date is null " + where_email_clause + " and " +
    "DATE_ADD(DATE(bp.payment_date), INTERVAL bp.reminder_days DAY) <= DATE(NOW())")


    

    #bills = Bill.objects.annotate(last_payment_date=Max('billpayment__payment_date'))
    #billpayments = BillPayment.objects.filter(payment_date__in[b.last_payment_date for b in bills])
    #billpayments = BillPayment.objects.filter(payment_date__in[b.last_payment_date for b in bills])

    #bills = Bill.objects.annotate(Max('billpayment__payment_date'))


    if process == True:
        pass
        #send emails and set flag
        #http://query7.com/tutorial-celery-with-django
    if request.is_ajax() or force_json:
        json = serializers.serialize("json", billpayments, relations=('bill',))
        return HttpResponse(json, "application/json")
    else:
        return render_to_response('BillMinder/alerts.html', context_instance=RequestContext(request))
    #return render_to_response('BillMinder/alerts.html', {'json': json}, context_instance=RequestContext(request))
