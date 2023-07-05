from pickle import LIST
from django.contrib.auth import login
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import chatmodel
from .forms import Signupform
# Create your views here.
def frontpage(request):
    return render(request,'core/frontpage.html')

def signup(request):
    if request.method=='POST':
        form=Signupform(request.POST)
        #print(form)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('frontpage')
    else:
        form=Signupform()
        return  render(request,'core/signup.html',{'form':form })

def Personalchatroom(request):
    final=[]
    currentuser=User.objects.filter(username=request.user.username)
    allusers=User.objects.all()    
    userlist=[x for x in list(allusers) if (x not in list (currentuser))]
    #user=User.objects.exclude(username=request.user.username)
    return render(request,'core/personalchat.html',{'userlists':userlist})

def personalroominside(request,username):
    print('heelllo')
    user_obj=User.objects.get(username=username)
    if request.user.id > user_obj.id:
        thread_name=f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name=f'chat_{user_obj.id}-{request.user.id}'
    messageobj=chatmodel.objects.filter(thread_name=thread_name)
   # print(messageobj)
    return render(request,'core/chat.html',{'other':user_obj,'messages':messageobj})