from django.contrib import admin
from .models import Picture, Blocked_Poster, Sms, Blocked_Number, Ad


admin.site.register(Picture)
admin.site.register(Blocked_Poster)
admin.site.register(Sms)
admin.site.register(Blocked_Number)
admin.site.register(Ad)
