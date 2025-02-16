from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Room, Topic

from .forms import RoomForm

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



    context = {'rooms': rooms, 'topics': topics, 'rooms_count': room_count}
    return render(request, 'base/home.html', context)


def room(request, pk):

    room = Room.objects.get(id=pk)
    
    
    topic= Topic.objects.all()
    
    context = {'rooms': room, 'topics' : topic}

    return render(request, 'base/room.html', context)




def createRoom(request):
    form = RoomForm()


    if request.method == 'POST':
        
        form = RoomForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')



    context = {'form' : form}
    
    return render(request, 'base/room_form.html', context )



def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)


    if request.method == 'POST':

        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()

            return redirect('home')
    

    context = {'form': form}
    
    return render(request, 'base/room_form.html', context)




def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    
    return render(request, 'base/delete.html', {'obj': room})




def loginPage(request):
    if request  == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

    try: 
        user = User.Object.get(username=username)
    except:
        messages.error(request, 'User not found')
    
    context = {}
    
    
    return render(request, 'base/login_register.html', context)


    
