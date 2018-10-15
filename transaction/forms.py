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
        Name = cleaned_data.get('full_ame')
        Account_No = cleaned_data.get('acc_No')
        Amount = cleaned_data.get('Amount')
        message = cleaned_data.get('message')
        
        if not Name and not Account_No and not message:
            raise forms.ValidationError('You have to write something!')
'''             
class trnsction(forms.Form):
    name = forms.CharField(max_length=30)
    acc_no = forms.IntegerField(label="acc_no")
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )
    amount = forms.IntegerField(label="Amount")

    def clean(self):
        name = self.cleaned_data.get('full_name')
        message = self.cleaned_data.get('message')
        acc_no=self.cleaned_data.get("acc_no")
<<<<<<< HEAD
        if not name and not message:
            raise forms.ValidationError('You have to write something!')
=======
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')'''
>>>>>>> 24a59c7d0ec26e8ba952e1caeb3b6b27a644416f
