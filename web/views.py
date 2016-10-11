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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from sorl.thumbnail import get_thumbnail
from django.core.files import File

import uuid
from varzeapro import settings

class LoginRequired(LoginRequiredMixin):
    login_url = 'web:login'
    redirect_field_name = None

class ShowTeam(LoginRequired, DetailView):
    model = Team
    template_name = "team.html"

class UpdateTeam(LoginRequired, UpdateView):
    form_class = TeamForm
    model = Team
    template_name = "edit_team.html"

class CreateTeam(LoginRequired, CreateView):
    success_message = 'Seu time foi criado com sucesso'
    form_class = TeamForm
    model = Team
    template_name = "new_team.html"

    def form_valid(self, form):
        if self.request.POST['logo_file_name'] != '':
            form.instance.logo = File(
                open(settings.MEDIA_TMP_DIR+self.request.POST['logo_file_name']),
                self.request.POST['logo_file_name']
            )
        return super(CreateTeam, self).form_valid(form)

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
            return redirect('web:index')
        else:
            messages.error(request, "Usuário ou senha inválidos")

        return render(request, "login.html")

class Logout(View):
    def get(self, request):
        logout(request)

        return redirect('web:login')

class Index(LoginRequired, TemplateView):
    template_name = "index.html"

class UploadFile(LoginRequired, View):
    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        file_name = '%s-%s' % (uuid.uuid4(), file.name)
        file_location = '%s%s' % (settings.MEDIA_TMP_DIR, file_name)

        with open(file_location, 'w') as f:
            f.write(file.read())

        thumbnail = get_thumbnail(file_location, '120x120', crop='center', quality=99)

        return JsonResponse({'message': 'File uploaded', 'file': file_name, 'thumbnail': thumbnail.url}, status=200)
