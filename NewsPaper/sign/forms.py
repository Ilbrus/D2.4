from django import forms
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class UpdateProfileForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]
        
class BasicSignupForm(SignupForm):
    
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='authors')
        basic_group.user_set.add(user)
        return user