from django import forms
from django.contrib.auth.models import User
from .models import Profile, NGO   
from django.contrib.auth.forms import UserCreationForm



class NGORegistrationForm(UserCreationForm):
    organization_name = forms.CharField(max_length=200, label="Organization Name")
    email = forms.EmailField(required=True, label="Organization Email")
    contact_person = forms.CharField(max_length=150, label="Contact Person Name")
    contact_number = forms.CharField(max_length=15, label="Contact Number")
    address = forms.CharField(widget=forms.Textarea, label="Address")

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')  

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['organization_name'].replace(" ", "_").lower()  
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            NGO.objects.create(
                user=user,
                name=self.cleaned_data['organization_name'],
                contact_person=self.cleaned_data['contact_person'],
                contact_number=self.cleaned_data['contact_number'],
                address=self.cleaned_data['address']
            )
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile_number','address']  


