from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from django.utils.safestring import mark_safe

from django.utils.timezone import datetime

SOFTWARE_TYPE = [
    (1, 'Atom'),
    (2, 'Bhartipay'),
]

class Software(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Machine'))
    mac = models.CharField(max_length=12, verbose_name=_('Mac Address'), unique=True)
    user = models.CharField(max_length=255, verbose_name=_('System User'))
    dt = models.DateTimeField(auto_now_add=True)
    message = models.TextField(null=True, blank=True)
    client = models.CharField(max_length=255)
    type = models.PositiveIntegerField(choices=SOFTWARE_TYPE)
    dt = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return '%s -> %s' % (self.name, self.user)

    def expiry(self):
        today = datetime.today()
        pk = Package.objects.filter(soft=self, from_dt__lte=today.date(), to_dt__gte=today.date())
        if not pk.exists():
            return mark_safe('<span style="color:red;">Expired</span>')
        elif pk:
            return pk[0].to_dt

class Package(models.Model):
    soft = models.ForeignKey(Software, on_delete=models.CASCADE, verbose_name='Software')
    from_dt = models.DateField(verbose_name=_('From Date'))
    to_dt = models.DateField(verbose_name=_('To Date'))
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    dt = models.DateTimeField(auto_now_add=True, verbose_name=_('Date & Time Added'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Last Updated'))

    def __str__(self):
        return '%s -> %s : %s - %s' %(self.soft.client, self.soft.get_type_display(), self.from_dt, self.to_dt)