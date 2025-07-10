from django.contrib import admin
from .models import TestQR, CertificateTemplate,TestResult


admin.site.register(TestQR)
admin.site.register(CertificateTemplate)
admin.site.register(TestResult)


# Register your models here.
