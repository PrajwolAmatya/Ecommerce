from django.contrib.auth.forms import UserCreationForm

from django.forms import ModelForm

from ecommerce.models import ProductReview


class SignUpForm(UserCreationForm):
    pass


class CommentForm(ModelForm):
    class Meta:
        model = ProductReview
        fields = ('rating', 'comment')
