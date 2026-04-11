# Register your models here.
from django.contrib import admin
from .models import Company, Tag, Contact, Interaction

admin.site.register(Company)
admin.site.register(Tag)
admin.site.register(Contact)
admin.site.register(Interaction)