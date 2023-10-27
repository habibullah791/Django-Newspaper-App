from django.db import models
from django.conf import settings
from django.urls import reverse


class Article(models.Model):
    """
    Article model represents a blog article.

    @desc: This model defines the attributes of a blog article, including the title, body, date of creation, and author. It also provides a method to get the absolute URL for viewing the article details.
    """

    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        """
        @desc: Returns a string representation of the article, which is its title.
        """
        return self.title

    def get_absolute_url(self):
        """
        @desc: Returns the absolute URL for viewing the details of the article.
        """
        return reverse("article_detail", kwargs={"pk": self.pk})


class Comments(models.Model):
    """
    Comments model represents comments on a blog article.

    @desc: This model represents comments made on a blog article. It is linked to the Article model and includes attributes for the comment text and the author of the comment. It also provides a method to get the absolute URL for viewing the list of articles.
    """

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        @desc: Returns a string representation of the comment, which is the comment text.
        """
        return self.comment

    def get_absolute_url(self) -> str:
        """
        @desc: Returns the absolute URL for viewing the list of articles.
        """
        return reverse("article_list")
