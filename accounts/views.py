from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import UserRegisterationForm
from .models import OtpCode
from utils import send_otp_code
import random

class UserRegisterView(View):
    form_class = UserRegisterationForm
    
    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/register.html', {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_code = random.randint(10000, 99999)
            send_otp_code(phone_number=cd['phone_number'], code=random_code)
            OtpCode.objects.create(phone_number=cd['phone_number'], otp_cpde=random_code)
            request.session['user_register_info'] = {
                'phone_number': cd['phone_number'],
                'full_name': cd['full_name'],
                'email': cd['email'],
                'password': cd['password']
            }
            messages.success(request, 'Weve sent you a verification code', 'success')
            return redirect('accounts:code_verify')
        return redirect('home:home')
        

class UserRegisterCodeVerifyView(View):

    def get(self, request):
        pass

    def post(self, request):
        pass