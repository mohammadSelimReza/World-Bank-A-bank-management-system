from typing import Any
from django import forms
from .models import TransactionModel

class TransactionForm(forms.ModelForm):
    class Meta:
        model = TransactionModel
        fields = ['ammount','transaction_type']
        
    def __init__(self,*args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput
        
    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()
    
    
class DepositForm(TransactionForm):
    def clean_ammount(self):
        min_deposit_ammount = 100
        ammount = self.cleaned_data["ammount"]
        if ammount < min_deposit_ammount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_ammount}$'
            )
        
        return ammount
    
class WithdrawForm(TransactionForm):
    def clean_ammount(self):
        account = self.account
        min_withdraw_ammount = 500
        max_withdraw_ammount = 20000
        balance = account.balance
        ammount = self.cleaned_data["ammount"]
        if ammount < min_withdraw_ammount:
            raise forms.ValidationError(
                f"You have to withdraw at least {min_withdraw_ammount}$"
            )
        if ammount > max_withdraw_ammount:
            raise forms.ValidationError(
                f"You can not withdraw more that {max_withdraw_ammount}$ at a time."
            )
        if ammount > balance:
            raise forms.ValidationError(
                f"You have {balance}$ in your account."
            )
        return ammount

class LoanRequestForm(TransactionForm):
    def clean_ammount(self):
        ammount = self.cleaned_data["ammount"]
        
        return ammount
    
    