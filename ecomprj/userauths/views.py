from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import User
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login, authenticate ,logout


def register_user(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, You Account was Created Successfully!")
            new_user = authenticate(username = form.cleaned_data["email"],
                         password = form.cleaned_data["password1"])
            login(request, new_user)
            return redirect("core:index")
    else:
        form = UserRegisterForm()
   
    context = {
      "form" : form,
      }
    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email = email)
            
            user = authenticate(request, email = email, password = password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are successfully logged In!")
                return redirect("core:index")
            else:
                messages.error(request, "User doesn't exist, Please Sign-Up")

        except:
            messages.error(request, f"User with {email} doesn't exist")

    return render(request, "userauths/sign-in.html")

def logout_view(request):
    logout(request)
    messages.success(request,"Logged Out Successfully!")
    return redirect("userauths:login")