from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    ACTIVE = 'active'
    NOT_ACTIVE = 'not_active'

    RESELLER_STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (NOT_ACTIVE, 'Not Active'),
    ]

    name = models.CharField(max_length=255)
    shopname = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=11)
    address = models.TextField()
    email_verified = models.BooleanField(default=False)
    reseller_status = models.CharField(
        max_length=10,
        choices=RESELLER_STATUS_CHOICES,
        default=NOT_ACTIVE
    )
    activation_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

class ActivationRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    reference = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    trxid = models.CharField(max_length=255)
    requested_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Activation request by {self.user.username}"
    





