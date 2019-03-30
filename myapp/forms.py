import base64
import re

from django import forms
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile

from myapp.models import Picture


class UploadForm(forms.ModelForm):
    """
    Form to upload the screenshot of a webpage
    """

    image_data = forms.CharField(widget=forms.HiddenInput(), required=False)
    image_file = forms.FileField(widget=forms.HiddenInput(), required=False)
    comment = forms.CharField(max_length=200, required=False)
    uploaded_by = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Picture
        fields = ['image_file', 'comment', 'uploaded_by']

    def clean(self):
        self.cleaned_data = super().clean()
        dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
        image_data = self.cleaned_data['image_data']
        image_data = dataUrlPattern.match(image_data).group(2)
        image_data = image_data.encode()
        image_file = ContentFile(base64.b64decode(image_data), name='screenshot.jpg')

        self.cleaned_data['image_file'] = image_file
        print(self.cleaned_data['image_file'])

        self.cleaned_data['uploaded_by'] = 'me'
        return self.cleaned_data
