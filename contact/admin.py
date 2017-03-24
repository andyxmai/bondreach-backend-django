from django.contrib import admin
from contact.models import Contact, FollowUp, Correspondence

class ContactAdmin(admin.ModelAdmin):
  search_fields = ('email', 'first_name', 'last_name',)

admin.site.register(Contact, ContactAdmin)
admin.site.register(FollowUp)
admin.site.register(Correspondence)