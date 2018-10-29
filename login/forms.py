import datetime
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
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
                  "designation",
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

class EmployeeRegistrationForm(UserCreationForm):
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
    acc_no = forms.IntegerField(label="Account Number")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        acc_no = self.cleaned_data.get("acc_no")
        password = self.cleaned_data.get("password")
        if acc_no and password:
                u_obj = User.objects.filter(acc_no=acc_no).first()
                if u_obj:
                    user = authenticate(email=u_obj.email, password=password)
                    if not user:
                        raise forms.ValidationError("Account Does Not Exist.")
                    if not user.check_password(password):
                        raise forms.ValidationError("Password Does not Match.")
                else:
                    raise forms.ValidationError("Account Does Not Exist.")
        return super(UserLoginForm, self).clean(*args, **kwargs)
    
class modifyacc(forms.Form):
    full_name = forms.CharField(
        max_length=50,
        widget=forms.Textarea(),
        label="Full_name"
    )
    email = forms.EmailField(label="EMAIL")
    contact_no = forms.IntegerField(label="Contact_Number")
    Address = forms.CharField(max_length=512,label="Enter your address")
    city = forms.CharField(max_length=256)
    def clean(self):
        full_name = self.cleaned_data.get('full_name')
        email = self.cleaned_data.get('email')
        contact_no=self.cleaned_data.get("contact_no")
        Address=self.cleaned_data.get("Address")
        city=self.cleaned_data.get("city")
