from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from .models import User, Profile
from .forms import UserRegisterForm, ProfileUpdateForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate ,logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from .email import send_email_verification
from django.contrib.auth import get_user_model
from .utils import EmailVerificationTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

User = get_user_model()

@csrf_exempt
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

@csrf_exempt
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

def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid:
            user_p = form.save(commit=False)
            user_p.user = request.user
            user_p.save()
            messages.success(request,"Profile Updated Successfully!")
            return redirect("core:dashboard")
    else:
            form = ProfileUpdateForm(instance=profile)
    context = {
        "form" : form,
        "profile" : profile,
    }
    return render(request,"userauths/profile-update.html", context)

@login_required
def change_password(request):
    user = request.user

    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Password Miss-Matched!!")
            return redirect("userauths:change-password")
        
        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password Changed Successfully")
            return redirect("userauths:login")
        else:
            messages.error(request, "Old Password is not correct")
            return redirect("userauths:change-password")
    return render(request, "userauths/change-password.html")

def email_verification_request(request):
    if not request.user.is_email_verified:
        send_email_verification(request, request.user.id)
        return HttpResponse("Email Verification link sent!")
    return HttpResponseForbidden("Email Already Verified!")

def email_verifier(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
        profile = Profile.objects.get(user=user)
    except:
        user = None
        profile = None

    if user == request.user:
        if EmailVerificationTokenGenerator.check_token(user, token):
            user.is_email_verified = True
            profile.verified = True
            user.save()
            profile.save()
            messages.success(request, "Profile Verified")
            return HttpResponseRedirect(reverse("userauths:profile-update"))
        return HttpResponseBadRequest("Invalid Request")
    
    return HttpResponseForbidden("You are not allowed to access this link")