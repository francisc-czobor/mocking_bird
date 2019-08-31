from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View


# Create your views here.

class IndexView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'index.html'

    def get(self, request):
        return render(request, 'index.html')


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('mock_login:index'))

        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('mock_login:index'))
        else:
            return HttpResponse('Invalid login details supplied!')


class LogoutView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'index.html'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('mock_login:login'))
