from django import forms
from .models import transaction
class trnsction(forms.ModelForm):
    class Meta:
        model = transaction
        fields = {
            "full_name",
            "acc_no",
            "Amount",
            "message",
        }
    def clean(self):
        cleaned_data = super(forms.ModelForm, self).clean()
        Name = cleaned_data.get('Name')
        Account_No = cleaned_data.get('Account_No')
        Amount = cleaned_data.get('Amount')
        message = cleaned_data.get('message')
        if not Name and not Account_No and not message:
            raise forms.ValidationError('You have to write something!')