from django import forms

class trnsction(forms.Form):
    name = forms.CharField(max_length=30)
    acc_no = forms.IntegerField(label="account_no")
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )
    amount = forms.IntegerField(label="amount")
   

    def clean(self):
        name = self.cleaned_data.get('name')
        message = self.cleaned_data.get('message')
        acc_no=self.cleaned_data.get("account_no")
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')