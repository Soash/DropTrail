from django.db import models
from tinymce.models import HTMLField

class Page(models.Model):
    contact_us = HTMLField()
    about_us = HTMLField()
    privacy_policy = HTMLField()

    def __str__(self):
        return "Page Information"




