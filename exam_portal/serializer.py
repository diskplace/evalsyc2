from rest_framework import serializers
from .models import CertificateTemplate

class CertificateSerilize(serializers.ModelSerializer):
    class Meta:
        model=CertificateTemplate
        fields=['id', 'webinar', 'img', 'title', 'subtitle', 'participant', 'host', 'subject', 'address', 'date']

