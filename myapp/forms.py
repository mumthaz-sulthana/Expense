from typing import Any
from django import forms

from myapp.models import Category,Transactions

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

class CategoryForm(forms.ModelForm):
    
    class Meta:
        
        model=Category
        
        fields=["name","budget"]
        
        widgets={
            
            "name":forms.TimeInput(attrs={"class":"form-control"}),
            
            "budget":forms.NumberInput(attrs={"class":"form-control"}),
            
            
        }
        
    def clean(self):
        
        self.cleaned_data=super().clean()
        
        budget_amount=self.cleaned_data.get("budget")
        
        if budget_amount < 150:
            
            self.add_error("budget","minimum budget should be 150")
            
        return self.cleaned_data
            
            
        
        
class TransactionForm(forms.ModelForm):
    
    class Meta:
        
        model=Transactions
        
        fields=["title","amount","category_object","payment_method"]
        
        widgets={
            
            "title":forms.TextInput(attrs={"class":"form-control mb-2"}),
            
            "amount":forms.NumberInput(attrs={"class":"form-control mb-2"}),
            
            "category_object":forms.Select(attrs={"class":"form-control form-select mb-2 "}),
            
            "payment_method":forms.Select(attrs={"class":"form-control form-select mb-2"}),
            
            
        }
        
class TransactionFilterForm(forms.Form):
    
    start_date=forms.DateField(widget=forms.DateInput(attrs={"type":"date","class":"form-control"}))
    
    end_date=forms.DateField(widget=forms.DateInput(attrs={"type":"date","class":"form-control"}))
    
    
class RegistrationForm(UserCreationForm):
    
    class Meta:
        
        model=User
        
        fields=["username","email","password1","password2"]
        
class LoginForm(forms.Form):
    
    username=forms.CharField()
    
    password=forms.CharField()
        
        
        
        
    
    
    
    