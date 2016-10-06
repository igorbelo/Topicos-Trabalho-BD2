# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login

class Login(View):
    def get(self, request):
        if request.user:
            return redirect('web:index')

        return render(request, "login.html")

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user and user.is_active:
            login(request, user)
            messages.success(request, "Bem-vindo")
            return redirect('web:index')
        else:
            messages.error(request, "Usuário ou senha inválidos")

        return render(request, "login.html")

class Index(TemplateView):
    template_name = "index.html"
