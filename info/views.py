from django.shortcuts import render
from .models import Page

def contact_view(request):
    page = Page.objects.first()
    return render(request, 'info/contact.html', {'content': page.contact_us})

def about_view(request):
    page = Page.objects.first()
    return render(request, 'info/about.html', {'content': page.about_us})

def policy_view(request):
    page = Page.objects.first()
    return render(request, 'info/policy.html', {'content': page.privacy_policy})
