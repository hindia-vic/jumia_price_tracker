from django.shortcuts import render,redirect
from .forms import CreateUser
from django.contrib import messages


def signup(request):
    form=CreateUser()
    context={'form':form}
    if request.method=='POST':
        form=CreateUser(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,"account succesfully created!")
            return redirect('home')

    return render(request,"registration/register.html",context)
            
# Create your views here.
