from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from blog_app.models import Post, Following, FollowedBy
# Create your views here.

user_name='' # global variable to store the present user.

def face(request):
    template_path = 'blog_app/face.html'
    context = {}
    return render(request,template_path,context)

def init_register(request):
    template_path = 'blog_app/init_register.html'
    context = {}
    return render(request, template_path, context)

def register(request):
    username = request.POST['username']
    email = request.POST['email']
    first_name = request.POST['first-name']
    last_name = request.POST['last-name']
    password = request.POST['password']

    try:
        user = User.objects.create_user(username,email,password)
    except IntegrityError as e:
        if 'UNIQUE constraint failed: auth_user.username' in e:
            # send user back to the registration view, with the error message.
            template_path = 'blog_app/init_register.html'
            context={
                'error_message':'Please select another username, the provided username has already been taken',
            }
            return render(request,template_path,context)
    else:
        user.first_name=first_name
        user.last_name=last_name
        user.save()
        # send user to the login view from here.
        #return HttpResponseRedirect(reverse('initLogin',args=[]))
        return redirect('initLogin')

def init_login(request):
    template_path='blog_app/init_login.html'
    context={}
    return render(request, template_path, context)

def login(request):
    global user_name
    username=request.POST['username']
    password=request.POST['password']
    user=auth.authenticate(username=username,password=password)
    if user is not None and user.is_active:
        user_name=str(username)
        auth.login(request,user)
        # send the user to the home view from here
        #return redirect('home')
        return HttpResponseRedirect(reverse('home', args=[user_name,]))
    else:
        template_path='blog_app/init_login.html'
        context={
            'error_message':'Invalid username or password. Please try again!'
        }
        return render(request,template_path,context)

def logout_view(request):
    auth.logout(request)
    return redirect('face')

@login_required(login_url='/blogit/')
def home(request,user):
    global user_name
    me=User.objects.get(username=user_name)
    other_user = User.objects.get(username=user)
    myposts = Post.objects.filter(user=me)[:5]  # display 5 posts
    other_user_posts = Post.objects.filter(user=other_user)
    follow_list = Following.objects.filter(user=me)  # return the list of the people the logged in user is following
    following_list = [ i.following for i in follow_list ]
    template_path = 'blog_app/home.html'
    context={
        'following_list': following_list,
        'real_user' : user_name,
        'other_user': user,
        'posts': myposts,
        'other_user_posts':other_user_posts,
    }
    return render(request,template_path,context)

@login_required(login_url='/blogit/')
def publish(request):
    global user_name
    me=User.objects.get(username=user_name)
    post_title = request.POST['post_title']
    post_body = request.POST['post_body']
    post = Post.objects.create(user=me, post_title=post_title, post_body=post_body)
    post.save()
    return HttpResponseRedirect(reverse('home', args=[user_name,]))

def post_details(request,user,post_id):
    post = get_object_or_404(Post, pk=post_id)
    template_path = 'blog_app/post_detail.html'
    context = {
        'post':post,
    }
    return render(request,template_path,context)

def all_posts(request, user):
    global user_name
    me = User.objects.get(username=user_name)
    myposts = Post.objects.filter(user=me)

    other_user = User.objects.get(username=user)
    other_user_post = Post.objects.filter(user=other_user)
    template_path = 'blog_app/all_posts.html'
    context = {
        'posts':myposts,
        'real_user':user_name,
        'other_user_posts':other_user_post,
        'other_user':user,
    }
    return render(request,template_path,context)

@login_required(login_url='/blogit/')
def follow(request, user):
    global user_name
    me = User.objects.get(username=user_name)
    following = Following.objects.create(user=me, following=user)
    following.save()

    other_user = User.objects.get(username=user)
    followed_by = FollowedBy.objects.create(user=other_user, followed_by=user_name)
    followed_by.save()

    #list_of_following = Following.objects.filter(user=me)
    
    return HttpResponseRedirect(reverse('home',args=[user_name,]))

@login_required(login_url='/blogit/')
def follow_list_view(request, user):
    #   DISPLAY THE LIST OF PEOPLE THE USER IS FOLLOWING
    #global user_name
    me = User.objects.get(username=user)
    following_list = Following.objects.filter(user=me)
    template_path = 'blog_app/follow_list.html'
    context = {
        'following_list': following_list,
    }
    return render(request,template_path,context)