from django.shortcuts import render,redirect, HttpResponseRedirect
from django.http import HttpResponse
from .models import Room,Topic, Message
from .forms import RoomForm, Userform
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

# rooms = [
#     {'id': 1, 'name': "Let Learning Python"},
#     {'id': 2, 'name': "Machine Learning with me"},
#     {'id': 3, 'name': "Hero to zero Deep Learning one video"},
# ]

def loginUser(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username= username)
        except:
            messages.error(request, 'User does not exit')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password does not exit")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Error during register account")
    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    # rooms = Room.objects.all()
    q = request.GET.get('q') if request.GET.get('q') else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q)
                                )
    room_count = rooms.count()
    topics = Topic.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics':topics,'room_count' : room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk = room.id)
    
    context = {'room': room, 'messages': messages, 'participants': participants}
    return render(request, 'base/room.html',context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        Room.objects.create(
            host=request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')
    topics = Topic.objects.all()
    context ={'form': form, 'topics' : topics}
    return render(request,'base/forms_room.html', context)


@login_required(login_url='login')
def upadate_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed update')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')
    
    topics = Topic.objects.all()
    context = {'form': form , 'topics' : topics , 'room' : room }
    return render(request, 'base/forms_room.html', context)



@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id =pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed update')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete_room.html', {'obj':room})


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id =pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed update')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete_room.html', {'obj':message})


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages' : room_messages , "topics" : topics }
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = Userform(instance=user)

    if request.method == 'POST':
        form = Userform(request.POST ,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk= user.id)
    return render(request, 'base/update-user.html',{'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains = q)
    context = {'topics' : topics }
    return render(request, 'base/topics.html', context)


def activitiesPage(request):
    room_message = Message.objects.all()
    context = {'room_message' : room_message }
    return render(request, 'base/activity.html')