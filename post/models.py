from django.db import models
from django.utils import timezone
from users.models import Profile

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=3000)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
    
    def __str__(self):
        return f'{" ".join(self.title.split()[:2])}... by {self.author}'
    
