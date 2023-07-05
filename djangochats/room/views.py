from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

from .models import Room,Messages
# Create your views here.
@login_required
def rooms(request):
    rooms=Room.objects.all()
    
    return render(request,'room/rooms.html',{'rooms':rooms})

@login_required
def create_room(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        slug=request.POST['code']
        roomname=request.POST['room']
        coded= Room.objects.filter(slug=slug).first()
    
        if coded == None:
            Room.objects.create(name=roomname,slug=roomname)
            return JsonResponse({
                'msg':'success'
            })
        else:
            print('exist')
            return JsonResponse({
                'msg':'notsuccess'
            })


        
       
#    if request.method=='POST':
 #       roomname=request.POST['room']
  #      Room.objects.create(name=roomname,slug=roomname)
   #     return redirect('rooms')
    #else:
    return render(request,'room/createroom.html')

@login_required
def room(request,slug):
    room=Room.objects.get(slug=slug)
    messages=Messages.objects.filter(room=room)[0:25]
        
    return render(request,'room/room.html',{'room':room,'messages':messages})

