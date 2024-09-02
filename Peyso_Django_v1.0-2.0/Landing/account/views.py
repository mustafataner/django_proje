from django.http import HttpResponse
from django.shortcuts import render


# Layouts Pages

def login(request):
    return render(request,"account/auth-login.html")
def recover_password(request):
    return render(request,"account/auth-recoverpw.html")
def register(request):
    return render(request,"account/auth-register.html")
from django.shortcuts import render, redirect
from .models import Contact

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Verileri kaydetme
        Contact.objects.create(name=name, email=email, subject=subject, message=message)

        # Başarıyla kaydedildikten sonra yönlendirme
        return redirect('success_page')  # success_page adında bir sayfaya yönlendirin
    return render(request, 'partials/contact.html')
