from django.contrib import admin
from .models import Webinar,WebinarAttendees,ResponseQuestionaire,TestResponse,Test_Question,Choice,Speaker

admin.site.register(Webinar)
admin.site.register(WebinarAttendees)
admin.site.register(ResponseQuestionaire)
admin.site.register(Test_Question)
admin.site.register(TestResponse)
admin.site.register(Choice)
admin.site.register(Speaker)


# Register your models here.
