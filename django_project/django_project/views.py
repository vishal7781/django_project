# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from datetime import datetime
from myapp.forms import signupform
from myapp.forms import loginform,PostForm,LikeForm,CommentForm
from imgurpython import ImgurClient
     
from django.contrib.auth.hashers import make_password,check_password
from myapp.models import usermode,sessiontoken,PostModel,LikeModel,CommentModel
from django_project.settings import BASE_DIR
import os
# Create your views here.
def signup_view(request):
    if request.method=='GET':
        #Display signup form       
         signup_form=signupform()
         
    elif request.method=='POST':
        #process the form data
        signup_form=signupform(request.POST)
        #Validate form data
        if signup_form.is_valid():
            #validation successful
            username=signup_form.cleaned_data['username']
            name=signup_form.cleaned_data['name']
            email=signup_form.cleaned_data['email']
            password=signup_form.cleaned_data['password']
            #save to db
            new_user=usermode(name=name,username=username,password=make_password(password),email=email)
            new_user.save()
            return redirect("/login/")

          

    return render(request,'signup.html', {'signup_form':signupform})


#login form
def login_view(request):
    response_data={}
    if request.method=="GET":
        #display login form
        login_form=loginform()
        #template_name='login.html'
    
    elif request.method=="POST":
        login_form=loginform(request.POST)
        if login_form.is_valid():
            #validation checks
            username=login_form.cleaned_data['username']
            password=login_form.cleaned_data['password']
            #fetch data from db
            user=usermode.objects.filter(username=username).first()
            if user:
                #password compare
                if check_password(password,user.password):
                    #login sucessfully
                    new_token=sessiontoken(user=user)
                    new_token.create_token()
                    new_token.save()
                    response=redirect('/feed/')
                    response.set_cookie(key='session_token',value=new_token.session_token)
                    return response
                    
                   # template_name='login_success.html'
                else:
                    #Does not login
                #    template_name='login_fail.html'
                    response_data['message'] = 'Incorrect password  ..! Please try again...'
        
    response_data['login_form']=loginform

    return render(request,'login.html',response_data)
    #        else:
                #user do not exists
     #           template_name='login_fail.html'
      #  else:
       #     print"validation failed"
        #    template_name='login_fail.html'

        
    #return render(request,template_name,{'login_form':login_form})

def feed_view(request):

    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('created_on')
        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:

                post.has_liked = True
        return render(request,'feed.html', { 'posts' : posts})
    else:
        return redirect('/login/')

def post_view(request):
    user = check_validation(request)
    form = PostForm()
    if user:
        if request.method == 'GET':
            form = PostForm()
            return render(request,'post.html',{'form': form})
        elif request.method == 'POST':
            form = PostForm(request.POST,request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                userpost = PostModel(user=user, image=image,caption=caption)
                userpost.save()
                print userpost.image.url
                path = os.path.join(BASE_DIR , userpost.image.url)
                print BASE_DIR
                print path
                client = ImgurClient('', '')
                userpost.image_url = client.upload_from_path(path,anon=True)['link']
                userpost.save()
                return redirect('/feed/')
            else:
                form = PostForm()
                return render(request, 'post.html',{'form': form})
    else:
        return redirect('/login/')


def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id

            existing_like = LikeModel.objects.filter(post_id=post_id,user=user).first()
           
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
                poster = PostModel.objects.filter(id=post_id).first()
                subject = "Your photo was liked"
                message = "Your photo was liked by" + " " +user.username
                from_email = EMAIL_HOST_USER
                to_email = [poster.user.email]
                send_mail(subject, message, from_email, to_email)
            else:
                existing_like.delete()
                poster = PostModel.objects.filter(id=post_id).first()
                subject = "Your photo was unliked"
                message = "Your photo was unliked by" + " " + user.username
                from_email = EMAIL_HOST_USER
                to_email = [poster.user.email]
                send_mail(subject, message, from_email, to_email)
            return redirect('/feed/')

    else:
        return redirect('/login/')

#comments in users post
def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user,post_id=post_id,comment_text=comment_text)
            comment.save()
            poster = PostModel.objects.filter(id=post_id).first()
            subject = "Comment on your photo"
            message = str(user.username) + " " + "commented on your photo" + " " + comment_text
            from_email = EMAIL_HOST_USER
            to_email = [poster.user.email]
            send_mail(subject, message, from_email, to_email)
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login/')


def check_validation(request):
    if request.COOKIES.get('session_token'):
        session=sessiontoken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user
        else:
            return None



