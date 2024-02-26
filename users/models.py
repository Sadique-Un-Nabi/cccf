from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from PIL import Image

import os
import shutil

    


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics/')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    cadet_name = models.CharField(max_length=15, blank=True, null=True)
    full_name = models.CharField(max_length=35, blank=True, null=True)
    intake = models.IntegerField(blank=True, null=True)
    admission_year = models.IntegerField(blank=True, null=True)
    college_name = models.CharField(max_length=50, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)
            
    def get_absolute_url(self):
        return reverse("post:home")



# Define the signal handler function
@receiver(pre_delete, sender=Profile)
def delete_profile_pics(sender, instance, **kwargs):
    # Get the username associated with the profile
    username = instance.user.username

    # Define the path to the user's profile pics directory
    profile_pics_dir = os.path.join('media', 'profile_pics', username)

    # Check if the directory exists and delete it
    if os.path.exists(profile_pics_dir):
        shutil.rmtree(profile_pics_dir)
