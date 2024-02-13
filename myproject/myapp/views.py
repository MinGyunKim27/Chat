from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .forms import RoomForm
from .models import Room
from django.urls import reverse


def index(request):
    return render(request, 'myapp/index.html')

@login_required
def video(request):
    return render(request, 'myapp/video.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
def list(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = RoomForm()
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms, 'form': form})

from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .models import Room

def delete_room(request, room_name):
    # 주어진 room_name을 가진 방을 데이터베이스에서 찾습니다.
    room = get_object_or_404(Room, name=room_name)
    
    # 방을 삭제합니다.
    room.delete()
    
    # 방을 삭제한 후, 관련 페이지로 리디렉션합니다.
    return redirect(reverse('index'))  # 예를 들어 홈 페이지로 리디렉션합니다.
