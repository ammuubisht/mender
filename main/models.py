from django.db import models

# Create your models here.
class MyList(models.Model):
    movie_title = models.TextField()
    movie_url = models.TextField()
    movie_thumbnail = models.ImageField()

    def __str__(self):
        return self.movie_title