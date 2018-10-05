import datetime
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms.extras.widgets import SelectDateWidget
from .models import User

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["full_name",
                  "gender",
                  "email",
                  "contact_no",
                  "Address",
                  "city",
                  "password1",
                  "password2"
                  ]

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['full_name']
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    account_no = forms.IntegerField(label="Account Number")
    password = forms.CharField(widget=forms.PasswordInput)
    if account_no and password:
            u_obj = User.objects.filter(account_no=account_no).first()
            if u_obj:
                user = authenticate(email=u_obj.email, password=password)
                if not user:
                    raise forms.ValidationError("Account Does Not Exist.")
                if not user.check_password(password):
                    raise forms.ValidationError("Password Does not Match.")
            else:
                raise forms.ValidationError("Account Does Not Exist.")
            
