from django.contrib import admin

from .models import *

admin.site.register(AUser)
admin.site.register(Account)
admin.site.register(Action)
admin.site.register(Transaction)
admin.site.register(Category)


