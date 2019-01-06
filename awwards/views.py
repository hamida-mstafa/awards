from __future__ import unicode_literals

from rest_framework.request import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import PostsSerializer,ProfileSerializer
from .permissions import IsAdminOrReadOnly
from django.shortcuts import render,redirect
from .forms import SignUpForm,ProfileForm,PostsForm,Comments,Votes
from .models import profile,Posts,Likes
from django.http import Http404

from django.contrib.auth.models import UserCreationForm
from django.contrib.auth import login,authenticate
# Create your views here.
def index(request):
    posts = Posts.objects.all()
    form = PostsForm()
    return render(request,'index.html',{"form":form,"posts":posts})

def signup(request):
    from = SignUpForm
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user=authenticate(username=username,email=email,password=password)
            user.save()
            profile=profile(user=user)
            profile.save()
            login(request,user)
            return redirect('/')
    return render(request,'signup.html',{"form":form})
    
