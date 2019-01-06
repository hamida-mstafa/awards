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

def profile(request):
    form = ProfileForm()
    current_user = Posts.objects.filters(user=current_user)
    profile = Profile.objects.get(user=current_user)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            message = 'Fill the form appropriately'
            return render(request,'profile/profile.html',{"profile":profile,"form":form,"message":message})
    return render(request,'profile/profile.html',{"form":form,"posts":posts,"profile":profile})

def posts(request):
        if request.method == 'POST':
                form = PostsForm(request.POST,request.FILES)
                if form.is_valid():
                        post = form.save(commit=False)
                        post.user = request.user
                        post.save()
                        return redirect('index')

        return redirect('index')

def get_post_by_id(request,id):
        post = Posts.objects.get(id=id)
        likes = Likes.objects.filter(post=post)
        design = []
        usability = []
        creativity = []
        content = []
        for x in likes:
                design.append(x.design)
                usability.append(x.usability)
                creativity.append(x.creativity)
                content.append(x.content)
        de = []
        us = []
        cre = []
        con = []

        if len(usability)>0:
                usa = (sum(usability)/len(usability))
                us.append(usa)
        if len(creativity)>0:
                crea = (sum(creativity)/len(creativity))
                cre.append(crea)
        if len(design)>0:
                des = (sum(design)/len(design))
                de.append(des)
        if len(content)>0:
                cont = (sum(content)/len(content))
                con.append(cont)

        comm = Comments()
        vote = Votes()
        if request.method == 'POST':

                vote_form = Votes(request.POST)
                if vote_form.is_valid():

                        design = vote_form.cleaned_data['design']
                        usability = vote_form.cleaned_data['usability']
                        content = vote_form.cleaned_data['content']
                        creativity = vote_form.cleaned_data['creativity']
                        rating = Likes(design=design,usability=usability,
                                        content=content,creativity=creativity,
                                        user=request.user,post=post)
                        rating.save()
                        return redirect('/')
        return render(request,'one.html',{"post":post,"des":des,"usa":usa,"cont":cont,"crea":crea, "vote":vote,"comm":comm})

def comment(request,id):
    post = Posts.objects.get(id=id)
    if request.method == 'POST':
        comm=Comments(request.POST)
        if comm.is_valid():
            comment=comm.save(commit=False)
            comment.user = request.user
            comment.post=post
            comment.save()
            return redirect('index')
    return redirect('index')

def profiles(request,id):
        user=User.objects.get(id=id)
        posts = Posts.objects.filter(user=user)
        return render(request,'profile/profiles.html',{"user":user,"posts":posts})
class PostList(APIView):
        def get(self,request,format=None):
                post = Posts.objects.all()
                serialized = PostsSerializer(post,many=True)
                return Response(serialized.data)

        def post(self,request,format=None):
                serializing = PostsSerializer(data=request.data)
                if serializing.is_valid():
                        serializing.save()
                        return Response(serialized.data,status=status.HTTP_201_CREATED)
                return Response(serialized.errors,status=staus.HTTP_401_BAD_REQUEST)



class ProfilesList(APIView):
        def get(self,request,format=None):
                postlist = Profile.objects.all()
                serialized = ProfileSerializer(postlist,many=True)
                return Response(serialized.data)


        def post(self,request,format=None):
                serializing = ProfileSerializer(data=request.data)
                if serializing.is_valid():
                        serializing.save()
                        return Response(serializing.data,status=status.HTTP_201_CREATED)
                return Response(serializing.errors,status=status.HTTP_401_BAD_REQUEST)

class ProfileData(APIView):
        permission_classes = (IsAdminOrReadOnly,)
        def get_profile(self, pk):
                try:
                        return Profile.objects.get(pk=pk)
                except Profile.DoesNotExist:
                        return Http404

        def get(self, request, pk, format=None):
                profile = self.get_profile(pk)
                serialized = ProfileSerializer(profile)
                return Response(serialized.data)

        def put(self,request,pk,format=None):
                profile = self.get_profile(pk)
                serializers = ProfileSerializer(profile,request.data)
                if serializers.is_valid():
                        serializers.save()
                        return Response(serializers.data)
                return Response(serializers.errors,status=ststus.HTTP_400_BAD_REQUEST)

        def delete(self,request,pk,format=None):
                profile = self.get_profile(pk)
                profile.delete()
                return Response(status=status.HTTP_204_BAD_REQUEST)
