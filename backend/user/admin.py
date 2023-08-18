from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Instructor)
admin.site.register(InstructorProfile)
admin.site.register(Course)
admin.site.register(Cart)
admin.site.register(Cartitems)
admin.site.register(WatchList)
admin.site.register(Watchitems)
admin.site.register(Review)
admin.site.register(Blog)
