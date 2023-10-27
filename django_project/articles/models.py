from django.db import models
from django.conf import settings
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    
    
    def __str__(self) -> str:
        return self.title
    
    
    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"pk": self.pk})


class Comments(models.Model):
    article =  models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    
    
    def __str__(self) -> str:
        return self.comment
    
    
    def get_absolute_url(self) -> str:
        return reverse("article_list")     