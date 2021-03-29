from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json


import mammoth
from .models import User, Paper, Comment, Community

# Create your views here.
@login_required(login_url='login')
def index(request, paper_id=0, view='read', user_id=0):
    papers = Paper.objects.filter(author=request.user)
    if paper_id != 0:
        my_paper = Paper.objects.filter(id=paper_id).first()
    else:
        my_paper = Paper.objects.filter(author=request.user).first()
    
    all_comments = Comment.objects.filter(paper=my_paper).order_by('-time_stamp')
    commenters = []
    for comment in all_comments:
        if comment.commenter not in commenters:
            commenters.append(comment.commenter)
    communities = Community.objects.filter(members__in=[request.user])

    if user_id == 0:
        comments = all_comments
    else:
        commenter = User.objects.filter(id=user_id).first()
        comments = Comment.objects.filter(commenter=commenter, paper=my_paper)

    return render(request, "index.html", {
        "papers": papers,
        "my_paper": my_paper,
        "comments": comments,
        "communities": communities,
        "commenters": commenters,
        "view": view,
        "selected_value": user_id
    })


@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        document = request.FILES['document']
        result = mammoth.convert_to_html(document)
        paper = Paper.objects.create(title=request.POST['title'], content=result.value, author=request.user)
        paper.save()
        return HttpResponseRedirect(reverse('index', kwargs={'paper_id': paper.id}))
    return HttpResponseRedirect(reverse('index'))


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html', {
                "message": "Invalid username and/or password."
        })
    
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
    
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, "login.html", {
                "message": "Passwords do not match"
            })
        user = User.objects.create_user(username, email, password)
        user.save() 
        login(request, user)

        return HttpResponseRedirect(reverse('complete_profile'))
    return render(request, 'login.html')


@login_required(login_url='login')
def compose(request):
    if request.method == 'POST':
        papers = Paper.objects.filter(author=request.user)
        communities = Community.objects.filter(members__in=[request.user])
        paper = Paper.objects.create(title="untitled", author=request.user)
        return render(request, 'compose.html', {
            'paper': paper,
            'papers': papers,
            'commmunites': communities
        })
    else:
        return HttpResponseRedirect(reverse('index'))



@login_required(login_url='login')
def add_comment(request, paper_id):
    if request.method == 'POST':
        paper = Paper.objects.get(id=paper_id)
        content = request.POST['comment']
        selection = request.POST['selection']
        comment = Comment.objects.create(commenter=request.user, paper=paper, content=content, selection=selection)
    return HttpResponseRedirect(reverse('index', kwargs={'paper_id': paper_id, 'view': 'comments'}))


@login_required(login_url='login')
def create_community(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        confirmation = request.POST['confirmation']

        if password != confirmation:
            return HttpResponse('Passwords do not match.')

        if Community.objects.filter(name=name).count() != 0:
            return HttpResponse(f'{name} is taken.')
        
        member = User.objects.get(id=request.user.id)
        print(member)
        community = Community.objects.create(admin=request.user, name=name, password=password)
        community.members.add(member)
        community.save()
        return HttpResponseRedirect(reverse('community', kwargs={'community_name': community.name}))
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='login')
def join_community(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        community = Community.objects.filter(name=name, password=password).first()
        if community:
            community.members.add(request.user)
            community.save()

        return HttpResponseRedirect(reverse('index'))


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url="login")
def community(request, community_name):
    community = Community.objects.filter(name=community_name).first()
    users = User.objects.all()
    members = []
    for user in users:
        user_communities = Community.objects.filter(members__in=[user])
        if community in user_communities:
            members.append(user)
    communities = Community.objects.filter(members__in=[request.user])
    papers = Paper.objects.filter(author=request.user)
    return render(request, 'community.html', {
        'community': community,
        'members': members,
        'communities': communities,
        'papers': papers
    })


@login_required(login_url="login")
def profile(request, username):
    profile = User.objects.filter(username=username).first()
    if not profile:
        return HttpResponse('User not found')
    papers = Paper.objects.filter(author=request.user)
    user_papers = Paper.objects.filter(author=profile)
    communities = Community.objects.filter(members__in=[request.user])
    user_communities = Community.objects.filter(members__in=[profile])
    return render(request, "profile.html", {
        'profile': profile,
        'papers': papers,
        'user_papers': user_papers,
        "communities": communities,
        "user_communities": user_communities
    })


@login_required(login_url="login")
def edit(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        paper = Paper.objects.filter(id=data['id']).first()
        paper.content = data['content']
        paper.save()
    return HttpResponse('')


@login_required(login_url="login")
def leave_community(request, community_id):
    if request.method == 'POST':
        community = Community.objects.filter(id=community_id).first()
        community.members.remove(request.user)
        community.save()
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url="login")
def filter_comments(request):
    if request.method == 'POST':
        paper_id = request.POST['paper-id']
        user_id = request.POST['user-id']
        if request.POST != 0:
            return HttpResponseRedirect(reverse('index', kwargs={'paper_id': paper_id, 'view': 'comments', 'user_id': user_id}))


@login_required(login_url="login")
def complete_profile(request):
    user = User.objects.filter(id=request.user.id).first()
    if request.method == 'POST':
        user.photo = request.POST['photo']
        user.bio = request.POST['bio']
        user.genre = request.POST['genre']
        user.influences = request.POST['influences']
        user.why = request.POST['why']
        user.what = request.POST['what']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "questions.html", {
            'user': user
        })


@login_required(login_url="login")
def change_title(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        paper = Paper.objects.filter(id=data['id']).first()
        paper.title = data['title']
        paper.save()
    return HttpResponse('')