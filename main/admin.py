from django.contrib import admin
from .models import Clients

class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_telegram_id', 'client_username', 'client_status', 'client_course_tarif', 'activation_end_date')
    list_filter = ('client_status', 'client_course_tarif', 'activation_end_date')
    search_fields = ('client_name', 'client_telegram_id', 'client_username', 'client_phon_number')

admin.site.register(Clients, ClientAdmin)
