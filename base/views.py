from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from .models import Room, Topic, Message

from .forms import RoomForm, UserForm

# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
   
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()


    room_count = rooms.count()


    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))




    context = {'rooms': rooms, 'topics': topics, 'rooms_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):

    room = Room.objects.get(id=pk)

    room_messages = room.messages.all().order_by('-created')
    

    participants = room.participants.all()



    
    
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )

        room.participants.add(request.user)

        return redirect('room',pk=room.id)
    
    context = {'rooms': room, 'room_messages': room_messages, 'participants': participants}

    return render(request, 'base/room.html', context)



@login_required(login_url='login')

def createRoom(request):
    form = RoomForm()


    if request.method == 'POST':
        
        form = RoomForm(request.POST)

        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')



    context = {'form' : form}
    
    return render(request, 'base/room_form.html', context )


@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here')


    if request.method == 'POST':

        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()

            return redirect('home')
    

    context = {'form': form}
    
    return render(request, 'base/room_form.html', context)



@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    
    return render(request, 'base/delete.html', {'obj': room})




def loginPage(request):
    page = 'login'
    
    
    if request.user.is_authenticated:
        return redirect('home')
    
    
    username = None
    password = None
    
    if request.method  == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

    try: 
        user = User.objects.get(username=username)
    except:
        messages.error(request, 'User not found')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('home')
    else: 
        messages.error(request, 'Username or password is incorrect')
    
    context = {'page' : page}
    
    
    return render(request, 'base/login_register.html', context)



def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    
    form=UserCreationForm()




    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured')

    
    return render(request, 'base/login_register.html',{'form':form})



    
@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('You are not allowed here')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    
    return render(request, 'base/room.html', {'obj': message})




def userProfile(request, pk):
    user = User.objects.get(id=pk)
    
    
    context = {'user': user}
    return render(request, 'C:/Users/trace/studybud/base/templates/base/profile.html', context)



@login_required
def updateUser(request):
    user = request.user
    form = UserForm(instance=request.user)


    if request.method == 'POST':
        
        form = UserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            redirect('user-profile', pk=user.id)
    
    return render(request, 'C:/Users/trace/studybud/base/templates/base/update-user.html')

def topicsPage(request):
    
    return render(request, 'base/topics.html', {})