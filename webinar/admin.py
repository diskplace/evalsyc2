from django.contrib import admin
from .models import Webinar,WebinarAttendees,ResponseQuestionaire

admin.site.register(Webinar)
admin.site.register(WebinarAttendees)
admin.site.register(ResponseQuestionaire)

# Register your models here.
