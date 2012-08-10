from django.db import models
from datetime import datetime

class Bill(models.Model):
    name = models.CharField(max_length=200)
    default_amount = models.DecimalField(decimal_places=2, max_digits=9)
    default_reminder_days = models.IntegerField()
    last_payment_date = models.DateTimeField(auto_now=False,null=True,blank=True)
    demo_access = models.BooleanField()
    def __unicode__(self):
        return self.name
    def natural_key(self):
        return (self.id, self.name)
    #@property
    def calculate_health(self):
        datediff = datetime.now() - self.last_payment_date
        return round((1.0 - (float(datediff.days) / float(self.default_reminder_days))),2)
    #@property
    def calculate_health_color(self):
        health_number = self.calculate_health()
        if health_number > 0.5:
            return 'green'
        elif health_number > 0.0:
            return 'yellow'
        else:
            return 'red'
    #@property
    def calculate_days(self):
        return (datetime.now() - self.last_payment_date).days
    health = property(calculate_health)
    health_color = property(calculate_health_color)
    days_since_payment = property(calculate_days)

    
class BillPayment(models.Model):
    bill = models.ForeignKey(Bill)
    payment_date = models.DateTimeField()
    payment_amount = models.DecimalField(decimal_places=2, max_digits=9)
    reminder_days = models.IntegerField()
    confirmation_number = models.CharField(max_length=200)
    notes = models.CharField(max_length=1000)
    reminder_email_sent = models.BooleanField()
    def __unicode__(self):
        return self.bill.name + " - $" + unicode(self.payment_amount) + " on " + unicode(self.payment_date)