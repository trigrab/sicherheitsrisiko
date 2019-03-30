from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import FormView, TemplateView

from myapp.forms import UploadForm
from myapp.models import Picture


class Upload(FormView):
    template_name = 'sicherheitsrisiko/upload.html'
    form_class = UploadForm
    success_url = '/gallery'

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class Gallery(TemplateView):
    template_name = 'sicherheitsrisiko/gallery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['pictures'] = Picture.objects.all()
        return context
