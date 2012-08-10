from HomeWeb.billminder.models import Bill, BillPayment #@UnresolvedImport
from django.contrib import admin

admin.site.register(Bill)
admin.site.register(BillPayment)