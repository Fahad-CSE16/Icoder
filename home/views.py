from django.shortcuts import render, HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post
import time

# Create your views here.

def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    
    if request.method== 'POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        if len(name)<2 or len(email)<11 or len(content)<4 or len(phone)<11:
            messages.error(request, 'Error! Please fill the form properly!')
        else:
            contact=Contact(name=name, phone=phone, content=content, email=email)
            contact.save()
            messages.success(request, 'Success! your message have been sent successfully.')

    return render(request, 'home/contact.html')

def search(request):
    query= request.GET['query']
    if len(query) > 78:
        myposts=Post.objects.none()
    else:
        mypoststitle=Post.objects.filter(title__icontains=query)
        mypostscontent=Post.objects.filter(content__icontains= query)
        myposts= mypoststitle.union(mypostscontent)
    return render(request, 'home/search.html',{'myposts':myposts, 'query':query})
    # return HttpResponse("This is our search page")

def handleSignup(request):
    if request.method== 'POST':
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if len(username) > 15:
            messages.error(request,"Error! Username Must be under 15 characters.")
            return redirect('home')
        if not username.isalnum():
            messages.error(request,"Error! Username can only contains letters and digits")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request,"Error! Password do not matvh! Please Enter same password twice.")
            return redirect('home')

        myuser= User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"Success! You have successfully signed up.")
        return redirect('home')
    else:
        return HttpResponse("error")    


def handleLogin(request):
    if request.method== 'POST':
        loginusername=request.POST['loginusername']
        loginpass=request.POST['loginpass']
        user= authenticate(username= loginusername, password= loginpass)
        if user is not None :
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect('home')
        else:
            messages.error(request, "Error! Please enter correct username and password!")
            return redirect('home')
    else:
        return HttpResponse("404! not found") 
        
def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('home')
