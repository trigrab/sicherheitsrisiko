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
        context['pictures'] = Picture.objects.filter(deleted=False).order_by('-id')[:50]
        return context


class SinglePhoto(TemplateView):
    template_name = 'sicherheitsrisiko/single_photo.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if not Picture.objects.filter(pk=kwargs['picture_id']).exists():
            return {}
        picture = Picture.objects.get(pk=kwargs['picture_id'])
        next_pic = picture.id + 1 if Picture.objects.filter(pk=picture.id+1).exists() else picture.id
        previous = picture.id - 1 if Picture.objects.filter(pk=picture.id-1).exists() else picture.id
        context = {
            'id': picture.id,
            'comment': picture.comment,
            'url': picture.image_file.path,
            'next': next_pic,
            'previous': previous,
        }
        return context
