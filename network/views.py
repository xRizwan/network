from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json

from .models import User, Post, Comment, Like, Following


def index(request):
    postsdata = Post.objects.all().order_by('-timestamp')
    loggedUser = ''
    if (request.user.is_authenticated):
        loggedUser = User.objects.get(username=request.user.username)

    p = Paginator(postsdata, 10)

    pagenumber = request.GET.get('page')

    if pagenumber == None:
        pagenumber = 1
    elif int(pagenumber) > int(p.num_pages):
        pagenumber = 1
    else:
        pagenumber = int(pagenumber)

    maindata = p.get_page(pagenumber)

    return render(request, "network/index.html", {
        'data': maindata,
        'loggedUser': loggedUser,
        'page_obj': maindata,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def newpost(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(login))

    if request.method == 'POST':
        print(request.POST["message"])
        by = User.objects.get(username=request.user.username)
        newPost = Post(message=request.POST["message"], by=by)
        newPost.save()

        return HttpResponseRedirect(reverse("index"))

    return render(request, 'network/newpost.html')

def userprofile(request, user_name):
    try:
        user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))

    try:
        following = Following.objects.get(user=user)
        totalfollowings = following.following.count
    except Following.DoesNotExist:
        following = []
        totalfollowings = 0

    posts = Post.objects.filter(by=user).order_by('-timestamp')
    p = Paginator(posts, 10)
    pagenumber = request.GET.get('page')
    if pagenumber == None:
        pagenumber = 1
    elif int(pagenumber) > int(p.num_pages):
        pagenumber = 1
    else:
        pagenumber = int(pagenumber)
    maindata = p.get_page(pagenumber)

    followers = Following.objects.filter(following__username=user.username)
    totalFollowers = followers.count

    isFollowed = False
    for f in followers:
        if f.user.username == request.user.username:
            isFollowed = True

    return render(request, 'network/profile.html', {
        'userData': user,
        'followersLength': totalFollowers,
        'followingLength': totalfollowings,
        'posts': maindata,
        'isFollowed': isFollowed,
    })

@login_required
def following(request):

    # get all(if any) users followed by the current user
    try:
        userfollows = Following.objects.get(user=request.user)
    except Following.DoesNotExist:
        userfollows = None

    # temporary list
    tempList = []

    # get all users that the current user is following
    if (userfollows != None):
        for user in userfollows.following.all():
            # get posts if any made by the followed users
            try:
                posts = Post.objects.filter(by=user)
                tempList.append(posts)
            except Post.DoesNotExist:
                continue
    
    # creating an empty query set and joining with all the other querysets obtained
    qs = Post.objects.none()
    for posts in tempList:
        qs = qs | posts # | is the joining operator for two query sets

    # sorting the query set
    qs = qs.order_by('-timestamp')

    p = Paginator(qs, 10)
    pagenumber = request.GET.get('page')
    if pagenumber == None:
        pagenumber = 1
    elif int(pagenumber) > int(p.num_pages):
        pagenumber = 1
    else:
        pagenumber = int(pagenumber)
    maindata = p.get_page(pagenumber)
    
    return render(request, 'network/following.html', {
        'data': maindata,
    })

# post information api route
@csrf_exempt
@login_required
def postinformation(request, post_id):
    try:
        # , by=request.user
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post Does Not Exist'}, status=400)
    
    if request.method == 'GET':
        return JsonResponse(post.serialize())
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get('message') is not None:
            post.message = data["message"]
        else:
            return JsonResponse({"error": 'Trying to set an empty message is not allowed'}, status=400)
        post.save()

        return JsonResponse({"message": "success"} ,status=200)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        if (data.get('like') is not None):
            print('liking')
            post = Post.objects.get(pk=post_id)
            isLiked = False

            try:
                Like.objects.get(likedBy=request.user, postId=post.id)
                isLiked = True
            except Like.DoesNotExist:
                isLiked = False

            if isLiked:
                refLike = Like.objects.get(likedBy=request.user, postId=post.id)
                deleted = post.likes.remove(refLike)
                refLike.delete()
                print('unliked')
                return JsonResponse({"message": "unliked"}, status=200)

            else:
                liked = Like(likedBy=request.user, postId=post.id)
                liked.save()
                post.likes.add(liked)
                print('liked')
                return JsonResponse({"message": "liked"}, status=200)
    
    else:
        return JsonResponse({
            'error': 'GET, PUT or POST request required'
        }, status=400)

@csrf_exempt
@login_required
def managefollowing(request, user_name):
    
    try:
        user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        return JsonResponse({'error': 'user does not exist'}, status=400)
    
    try:
        userFollowing = Following.objects.get(user=request.user)
        if userFollowing.following.filter(username=user_name).count() > 0:
            isFollowed = True
        else:
            isFollowed = False

    except Following.DoesNotExist:
        userFollowing = Following(user=request.user)
        userFollowing.save()
        isFollowed = False

    if request.method == 'GET':
        return JsonResponse({'message': 'success'}, status=200)

    elif request.method == 'POST':
        data = json.loads(request.body)

        if data.get("follow") is not None:
            if isFollowed:
                userinquestion = User.objects.get(username=user_name)
                found = userFollowing.following.remove(userinquestion)
                return JsonResponse({'message': 'unfollowed'}, status=200)
            else:
                userFollowing.following.add(user)

        return JsonResponse({'message': 'followed'}, status=200)
    
    else:
        return JsonResponse({'warning': 'Only Get or Post request allowed!'}, status=400)
