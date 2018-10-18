from django import forms
from transaction.models import TX_in

class trnsction(forms.ModelForm):
    class Meta:
        model = TX_in
        fields = {
            "fullname",
            "acc_no",
            "Amount",
            "message",
        }
    def clean(self):
        cleaned_data = super(forms.ModelForm, self).clean()
        Name = cleaned_data.get('full_name')
        Account_No = cleaned_data.get('acc_no')
        Amount = cleaned_data.get('Amount')
        message = cleaned_data.get('message')
        
        if not Name and not Account_No and not message:
<<<<<<< HEAD

=======
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
<<<<<<< HEAD
>>>>>>> 6281daa25f7824d3b1493247929f4a2dbcd6c807
class trnsction(forms.Form):
    name = forms.CharField(max_length=30)
=======
class addMoney(forms.Form):
    Amount = forms.IntegerField(label="Amount")
>>>>>>> 1b47abb3cb7f02de5da4cd97eabbe54774b43c90
    acc_no = forms.IntegerField(label="acc_no")
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )
<<<<<<< HEAD
<<<<<<< HEAD
    amount = forms.IntegerField(label="amount")
   
=======
    amount = forms.IntegerField(label="Amount")
>>>>>>> 6281daa25f7824d3b1493247929f4a2dbcd6c807

=======
>>>>>>> 1b47abb3cb7f02de5da4cd97eabbe54774b43c90
    def clean(self):
        amount = self.cleaned_data.get('Amount')
        message = self.cleaned_data.get('message')
        acc_no=self.cleaned_data.get("acc_no")
<<<<<<< HEAD
        if not name and not email and not message:
<<<<<<< HEAD
            raise forms.ValidationError('You have to write something!')
=======
            raise forms.ValidationError('You have to write something!')'''
>>>>>>> 6281daa25f7824d3b1493247929f4a2dbcd6c807
=======
        if not amount and not acc_no:
            raise forms.ValidationError('You have to write something!')
>>>>>>> 1b47abb3cb7f02de5da4cd97eabbe54774b43c90
