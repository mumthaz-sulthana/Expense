from django.shortcuts import render,redirect

from django.views.generic import View

from django.utils import timezone

from myapp.forms import CategoryForm,TransactionForm,TransactionFilterForm,RegistrationForm,LoginForm

from myapp.models import Category,Transactions

from django.db.models import Sum

from django.contrib.auth import authenticate,login,logout

# Create your views here.

class CategoryCreateView(View):
    
    def get(self,request,*args,**kwargs):
        
        form_instance=CategoryForm()
        
        qs=Category.objects.filter(owner=request.user)
        
        return render(request,"category_add.html",{"form":form_instance,"categories":qs})
    
    def post(self,request,*args,**kwargs):
        
        form_instance=CategoryForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.instance.owner=request.user
            
            cat_name=form_instance.cleaned_data.get("name")
            
            user_object=request.user
            
            is_exist=Category.objects.filter(name__iexact=cat_name,owner=user_object).exists()
            
            
            if is_exist:
                
                print("category already exist under the user")
                
                return render(request,"category_add.html",{"form":form_instance,"message":"category already exist"})
                
            else:
                
                 form_instance.save()
                 
                 return redirect("category-add")
                
        else:
            
            return render(request,"category_add.html",{"form":form_instance})
        
class CategoryEditView(View):
    
    
    def get(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")
        
        category_object=Category.objects.get(id=id)
        
        form_instance=CategoryForm(instance=category_object)
        
        return render(request,"category_edit.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")
        
        category_object=Category.objects.get(id=id)
        
        form_instance=CategoryForm(request.POST,instance=category_object)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            return redirect("category-add")
        else:
            return render(request,"category_edit.html",{"form":form_instance})
        
class TransactionCreateView(View):
    
    def get(self,request,*args,**kwargs):
        
        form_instance=TransactionForm()
        
        cur_month=timezone.now().month
        
        cur_year=timezone.now().year
        
        categories=Category.objects.filter(owner=request.user)
        
        qs=Transactions.objects.filter(created_date__month=cur_month,created_date__year=cur_year,owner=request.user)
        
        return render(request,"transaction_add.html",{"form":form_instance,"transactions":qs,"categories":categories})
    
    def post(self,request,*args,**kwargs):
        
        form_instance=TransactionForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.instance.owner=request.user
            
            form_instance.save()
            
            return redirect("transaction-add")
        
        else:
            return render(request,"transaction_add.html",{"form":form_instance})

class TransactionUpdateView(View):
    
    def get(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")
        
        trans_obj=Transactions.objects.get(id=id)
        
        form_instance=CategoryForm(instance=trans_obj)
        
        return render(request,"transaction_edit.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")
        
        trans_obj=Category.objects.get(id=id)
        
        form_instance=CategoryForm(request.POST,instance=trans_obj)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            return redirect("transaction-add")
        else:
            return render(request,"transaction_edit.html",{"form":form_instance})
        
class TransactionDeleteView(View):
    
    def get(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")
        
        Transactions.objects.get(id=id).delete()
        
        return redirect("transaction-add")

class ExpenseSummaryView(View):
    
    def get(self,request,*args,**kwargs):
        
        cur_month=timezone.now().month
        
        cur_year=timezone.now().year
        
        qs=Transactions.objects.filter(
            created_date__month=cur_month,
            created_date__year=cur_year
        )
        
        total_expense=qs.values("amount").aggregate(total=Sum("amount"))#{"total":123456}
        
        category_summary=qs.values("category_object__name").annotate(total=Sum("amount"))
        
        payment_summary=qs.values("payment_method").annotate(total=Sum("amount"))
        
        print(payment_summary)
        
        
        
        data={
            "total_expense":total_expense.get("total"),
            
            "category_summary":category_summary,
            
            "payment_summary":payment_summary
            
           
       }
        
        return render(request,"expense_summary.html",data)
    
    
class TransactionSummaryView(View):
    
    def get(self,request,*args,**kwargs):
        
        form_instance=TransactionFilterForm()
        
        cur_month=timezone.now().month
        
        cur_year=timezone.now().year
        
        if "start_date" in request.GET and "end_date" in request.GET:
            
            start_date=request.GET.get("start_date")
            
            end_date=request.GET.get("end_date")
            
            qs=Transactions.objects.filter(
                                            created_date__range=(start_date,end_date)
                                           )
            
        else:
        
            qs=Transactions.objects.filter(
                                        created_date__month=cur_month,
                                        created_date__year=cur_year)
                                       
        
        return render(request,"transaction_summary.html",{"transactions":qs,"form":form_instance})
    
class ChartView(View):
    
    def get(self,request,*args,**kwargs):
        
        return render(request,"chart.html")
    
class SignUpView(View):
    
    def get(self,request,*args,**kwargs):
        
        form_instance=RegistrationForm()
        
        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):
        
        form_instance=RegistrationForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            print("account created successfully")
            
            return redirect("signin")
        else:
            print("failed to create account")
            
            return render(request,"register.html",{"form":form_instance})
        
class SignInView(View):
    
    def get(self,request,*args,**kwargs):
        
        form_instance=LoginForm()
        
        return render(request,"login.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):
        
        form_instance=LoginForm(request.POST)
        
        if form_instance.is_valid():
            
            user_obj=authenticate(request,**form_instance.cleaned_data)
            
            if user_obj:
                
                login(request,user_obj)
                
                return redirect("summary")
            
        return render(request,"login.html",{"form":form_instance})
    
class SignOutView(View):
    
    def get(self,request,*args,**kwargs):
        
        logout(request)
        
        return redirect("signin")
                
                
            
            
            
        
        
    
    
            
            
            
    
        
        
        
        
        
        