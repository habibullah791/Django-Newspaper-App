from django import forms
from .models import Comments

class CommentForm(forms.ModelForm):
    """
    CommentForm is a form for adding comments to a model.

    @param: forms.ModelForm (Django form)
    @desc: This form is used for adding comments to the Comments model. It includes fields for the comment content and the author's name. It allows users to submit comments on a specific model instance.
    @returns: A form for creating and submitting comments.
    """
    class Meta:
        model = Comments
        fields = ("comment", "author")
