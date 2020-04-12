from django.contrib import admin


from .models import User, upthing, Yzm, upneed


# Register your models here.
admin.site.register(upthing),
admin.site.register(User)
admin.site.register(Yzm),
admin.site.register(upneed)
