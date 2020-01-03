from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from apps.usuarios.models import Perfil
from apps.usuarios.forms import ProfileForm

# def user_profile(request):
#     _settings_keys = ('report_body_font',)
#     _values_to_print = {k:getattr(request.user.perfil, k) for k in dir(request.user.perfil) if k in _settings_keys}
#     return HttpResponse(f'{_values_to_print}')

class ProfileDetailView(DetailView):

    template_name = 'perfil_ver.html'

    def get_object(self):
        return get_object_or_404(Perfil, user=self.request.user)

class ProfileUpdate(UpdateView):

    fields = ['report_title_font', 'report_subtitle_font', 'report_body_font', 'report_color_title', 'report_bg_title']
    
    template_name = 'perfil_editar.html'
    extra_context={
        'title': 'Perfil de usuario',
        }

    #print(dir(UpdateView))

    def get_object(self):
        return get_object_or_404(Perfil, user=self.request.user)


