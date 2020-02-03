from django.db import models


class News(models.Model):
    img_link = models.TextField(blank=True)
    headline = models.TextField(max_length=300)
    text = models.TextField()
    source_link = models.TextField(max_length=100, unique=True)