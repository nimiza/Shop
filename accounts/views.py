from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import UserRegisterationForm, VerifyCodeForm
from .models import OtpCode, User
from utils import send_otp_code
import random

class UserRegisterView(View):
    form_class = UserRegisterationForm
    
    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/register.html', {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        print('before form')
        if form.is_valid():
            cd = form.cleaned_data
            random_code = random.randint(10000, 99999)
            send_otp_code(phone_number=cd['phone_number'], code=random_code)
            OtpCode.objects.create(phone_number=cd['phone_number'], otp_code=random_code)
            print('otp_code created')
            request.session['user_register_info'] = {
                'phone_number': cd['phone_number'],
                'full_name': cd['full_name'],
                'email': cd['email'],
                'password': cd['password']
            }
            messages.success(request, 'Weve sent you a verification code', 'success')
            return redirect('accounts:code_verify')
        print('After form - form is not valid')
        return redirect('home:home')
        

class UserRegisterCodeVerifyView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify_code.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_register_info']
        code_instance = OtpCode.objects.get(phone_number = user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            if cd['code'] == code_instance.otp_code:
                User.objects.create(email=user_session['email'], phone_number=user_session['phone_number'],
                                    full_name=user_session['full_name'], password=user_session['password'])
                messages.success(request, 'You Are Now Registered!', 'success')
            else:
                messages.error(request, 'Verify Code Was Wrong!', 'danger')

            code_instance.delete()
        return redirect('accounts:user_register')