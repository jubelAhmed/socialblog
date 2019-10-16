from django.shortcuts import render
from authApp.forms import UserForm,UserProfileInfoForm

# for login import
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect



# Create your views here.

def index(request):
    dic = {'title':'home'}
    return render(request,'authApp/index.html',context=dic)

@login_required
def special(request):
    return HttpResponse("You are logged in , Thanks for comming")

@login_required 
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
 
def register(request):
    registered = False
   
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit = False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
                 
            profile.save()
            
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
        
    dic = {'title':'registration','registered':registered,'user_form':user_form,'profile_form':profile_form}
    return render(request,'authApp/registration.html',dic)



def user_login(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username= username,password = password)
        
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('special'))
            else:
                return HttpResponse("Acount not active")
        
        else:
            print("someone tried to log in and failed! ")
            print("user name: {} and password is {} ".format(username,password))
            return HttpResponse("invalid login details supplied ! ")
        
    else:
        dict = {"title":"login"}
        return render(request,'authApp/login.html',dict) 
         
        
