from django import forms
from transaction.models import TX_in

class trnsction(forms.ModelForm):
    class Meta:
        model = TX_in
        fields = {
            "full_name",
            "acc_no",
            "Amount",
            "message",
            "OTP",
        }
    def clean(self):
        cleaned_data = super(forms.ModelForm, self).clean()
        Name = cleaned_data.get('full_name')
        Account_No = cleaned_data.get('acc_no')
        Amount = cleaned_data.get('Amount')
        message = cleaned_data.get('message')
        OTP = cleaned_data.get('OTP')
        if not Name and not Account_No and not message:
            raise forms.ValidationError('You have to write something!')


'''class addMoney(forms.ModelForm):
    class Meta:
        model = addmoney_own
        fields = {
            "acc_no",
            "Amount",
            "message",
        }
    def clean(self):
        cleaned_data = super(forms.ModelForm, self).clean()
        
        Account_No = cleaned_data.get('acc_No')
        Amount = cleaned_data.get('Amount')
        message = cleaned_data.get('message')
        
        if  not Account_No and not message and not Amount:
            raise forms.ValidationError('You have to write something!')
'''             
class addMoney(forms.Form):
    Amount = forms.IntegerField(label="Amount")
    acc_no = forms.IntegerField(label="acc_no")
    OTP=forms.IntegerField(label="OTP")
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )
    def clean(self):
        amount = self.cleaned_data.get('Amount')
        message = self.cleaned_data.get('message')
        acc_no=self.cleaned_data.get("acc_no")
        OTP = self.cleaned_data.get('OTP')
        if amount and not message:
            raise forms.ValidationError('You have to write something!')

class transferMerch(forms.Form):
    Amount = forms.IntegerField(label="Amount")
    from_acc_no = forms.IntegerField(label="from_acc_no")
    to_acc_no = forms.IntegerField(label="to_acc_no")
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )
    full_name=forms.CharField(
        max_length=2000,
    )
    def clean(self):
        Amount = self.cleaned_data.get('Amount')
        message = self.cleaned_data.get('message')
        from_acc_no=self.cleaned_data.get("from_acc_no")
        to_acc_no=self.cleaned_data.get("to_acc_no")
        full_name=self.cleaned_data.get("full_name")
        if Amount and not message:
            raise forms.ValidationError('You have to write something!')

'''class debitMoney(forms.ModelForm):
    class Meta:
        model = debitmoney
        fields = {
            "acc_no",
            "Amount",
            "message",
        }
    def clean(self):
        cleaned_data = super(forms.ModelForm, self).clean()
        
        Account_No = cleaned_data.get('acc_No')
        Amount = cleaned_data.get('Amount')
        message = cleaned_data.get('message')
        
        
        if not amount and not acc_no:
            raise forms.ValidationError('You have to write something!')
'''

class debitMoney(forms.Form):
    Amount = forms.IntegerField(label="Amount")
    acc_no = forms.IntegerField(label="acc_no")
    OTP=forms.IntegerField(label="OTP")
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )
    def clean(self):
        amount = self.cleaned_data.get('Amount')
        message = self.cleaned_data.get('message')
        acc_no=self.cleaned_data.get("acc_no")
        OTP = self.cleaned_data.get('OTP')
        if amount and not message:
            raise forms.ValidationError('You have to write something!')
            