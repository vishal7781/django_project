
from django import forms
from models import usermode,PostModel,LikeModel,CommentModel

class signupform(forms.ModelForm):
    class Meta:
        model = usermode
        fields = ['username','name','email','password']
class loginform(forms.ModelForm):
    class Meta:
        model=usermode
        fields=['username','password']
class PostForm(forms.ModelForm):
    class Meta:
        model=PostModel
        fields=['image','caption']
class LikeForm(forms.ModelForm):
    class Meta:
        model=LikeModel
        fields=['post']
class CommentForm(forms.ModelForm):
    class Meta:
        model=CommentModel
        fields=['comment_text','post']

