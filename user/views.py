from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import RedirectView,FormView,DetailView
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views import View
# Create your views here.

def send_mail(user,subject,template):
    message = render_to_string(template,{
        'user':user,
    })
    send_mail = EmailMultiAlternatives(subject,'',to=[user.email])
    send_mail.attach_alternative(message,"text/html")
    send_mail.send()

class UserSignupView(FormView):
    template_name = 'signup.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name= 'login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
# class UserLogoutView(LogoutView):
#     def get_success_url(self):
#         if self.request.user.is_authenticated:
#             logout(self.request)
#         return reverse_lazy('home')



def user_logout(request):
    logout(request)
    messages.success(request,'Logged out successfully')
    return redirect('home')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')    

class UserAccountUpdate(LoginRequiredMixin,View):
    template_name = 'update.html'

    def get(self,request):
        form = UserUpdateForm(instance = request.user)
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form = UserUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"Profile Updated Successfully!!")
            return redirect('profile')
        return render(request,self.template_name,{'form':form})

class PasswordChange(View):
    template_name = 'Change_pass.html'

    def get(self,request):
        form = PasswordChangeForm(user=request.user)
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form = PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Password Updated successfully!!")
            send_mail(request.user,"Password Change",'passchange_email.html')
            return redirect('profile')
        return render(request,self.template_name,{'form':form})
    
class Profileview(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'
    pk_url_kwarg = 'id'
    
   