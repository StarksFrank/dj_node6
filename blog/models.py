from django.db import models
from django.urls import reverse  # < here
from django.utils.text import slugify  # < here
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from imagekit.models import ImageSpecField
# here
from pilkit.processors import ResizeToFill
import logging

 
# Create your models here.
class Post(models.Model):  # < here
    """
    source='image' specifies the source image field
    ResizeToFill(700, 150) resizes and crops the image to size 700 x 150 pixels.
    quality specifies the JPEG quality
    """
    title = models.CharField(default='', max_length=255)
    body = models.TextField(default='', blank=True)
    slug = models.SlugField(default='', blank=True, max_length=255)
    # here ForeignKey And Dates
    date = models.DateTimeField(auto_now_add=True, null=True)
    # here ForeignKey And Dates
    updated = models.DateTimeField(auto_now=True, null=True)
    # here ForeignKey And Dates
    author = models.ForeignKey(User,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    tags = TaggableManager()
    image = models.ImageField(default='',
                              blank=True,
                              upload_to='images')
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(700, 150)],
                                     format='JPEG',
                                     options={'quality': 60})
    description = models.TextField(default='',
                                   blank=True)

    logging.info(f"models enter...")
    def __str__(self):
        return self.title

    def save(self, *args, **kwagrs):
        self.slug = slugify(self.title)
        super().save(*args, **kwagrs)

    def get_absolute_url(self):
        return reverse('blog:detail', args=[str(self.slug)])
