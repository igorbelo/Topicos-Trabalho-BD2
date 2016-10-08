# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, CreateView
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from core.models import Team
from web.forms import TeamForm

class ShowTeam(DetailView):
    model = Team
    template_name = "team.html"

class UpdateTeam(UpdateView):
    form_class = TeamForm
    model = Team
    template_name = "edit_team.html"

class CreateTeam(CreateView):
    success_message = 'Seu time foi criado com sucesso'
    form_class = TeamForm
    model = Team
    template_name = "new_team.html"

    def get_success_url(self):
        return reverse('web:team', args=(self.object.id,))

class Login(View):
    def get(self, request):
        if request.user and request.user.is_active and not request.user.is_anonymous:
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

class Logout(View):
    def get(self, request):
        logout(request)

        return redirect('web:login')

class Index(TemplateView):
    template_name = "index.html"
