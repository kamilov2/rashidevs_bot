# models.py
from django.db import models

import uuid




class Clients(models.Model):
    client_name = models.CharField(max_length=100)
    client_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    client_telegram_id = models.CharField(max_length=100)
    client_username = models.CharField(max_length=100, blank=True, null=True)
    client_status = models.BooleanField(default=False)
    client_check_time = models.TimeField(blank=True, null=True, auto_now_add=True)
    client_check_photo = models.ImageField(upload_to='check_photo/', blank=True, null=True) 
    client_phon_number = models.CharField(max_length=100, blank=True, null=True)
    client_course_tarif = models.BooleanField(default=False)
    activation_end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.client_id} | {self.client_name} | {self.client_id}'

    def short_client_id(self):
        return str(self.client_id)[:5]

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
