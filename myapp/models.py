import base64
import os

from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from PIL import Image

# Create your models here.
from sicherheitsrisiko import settings

THUMB_SIZE = (400, 400)


class Picture(models.Model):
    image_file = models.ImageField(upload_to='pictures', blank=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    upload_time = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    uploaded_by = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='thumbnails', editable=False)

    def save(self, *args, **kwargs):
        """
        Make and save the thumbnail for the photo here.
        """
        self.make_thumbnail()
        super().save(*args, **kwargs)

    def make_thumbnail(self):
        """
        Create and save the thumbnail for the photo (simple resize with PIL).
        """
        if self.thumbnail.name:
            print(self.thumbnail)
            return
        with open(self.image_file.path, 'r') as f:
            image = Image.open(self.image_file.path)
            image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

        # Path to save to, name, and extension
        thumb_name, thumb_extension = os.path.splitext(self.image_file.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            raise Exception('Could not create thumbnail - is the file type valid? ' + thumb_extension)

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # Load a ContentFile into the thumbnail field so it gets saved
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=True)
        temp_thumb.close()
