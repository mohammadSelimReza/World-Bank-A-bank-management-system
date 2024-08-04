from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import TransactionModel
from .forms import DepositForm,WithdrawFrom,LoadRequestForm
from .constrant import LOAN,DEPOSIT,LOAN_PAID,WITHDRAWAL
# Create your views here.
class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    template_name = ''
    model = TransactionModel
    title = ''
    success_url = ''
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account' : self.request.user.account,
        })
        return kwargs
    
    def get_conext_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })
        
class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = "Deposit"
    
    def get_initial(self):
        
        initial = {'transaction_type':DEPOSIT}
        return initial
    
    def form_valid(self, form):
        ammount = form.cleaned_data.get('ammount')
        account = self.request.user.account
        account.balance += ammount
        account.save(
            update_fields = ['balance']
        )
        
        return super().form_valid(form)

class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawFrom
    title = "Withdraw"
    
    def get_initial(self):
        
        initial = {'transaction_type':WITHDRAWAL}
        return initial
    
    def form_valid(self, form):
        ammount = form.cleaned_data.get('ammount')
        account = self.request.user.account
        account.balance -= ammount
        account.save(
            update_fields = ['balance']
        )
        
        return super().form_valid(form)
       