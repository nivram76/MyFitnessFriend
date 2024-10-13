from django.shortcuts import render, redirect
from django.db.models import Q
from.models import Room, Topic, Message
from .forms import RoomForm, TDEEForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

import re


# Create your views here.

#API KEY: u5vq9UaMtsQa6ItWSEISiA==jJ9dmq2jaz4bkpXV


# Room IDs:


def loginPage(request):

    page= 'login'
    # if user is already logged in just redirect
    if request.user.is_authenticated:
        return redirect('forums') # CHANGE TO HOME
    
    if request.method == 'POST':
        username= request.POST.get('username').lower()
        password= request.POST.get('password')

        try: # check if username is valid
            user = User.objects.get(username= username)
        
        except:
            messages.error(request, "User does not exist")

        
        user = authenticate(request, username= username, password= password)

        if user is not None: # user is a real user with valid credentials so log them in
            login(request, user)
            return redirect('home') 
 
        else: # not valid credentials
            messages.error(request, "Username or password doesn't exist.")



    context= {'page': page}
    return render(request, 'counter/login_register.html', context)





def logoutUser(request):

    logout(request)
    return redirect('forums') # CHANGE TO HOME PAGE LATER




def registerUser(request):
    form= UserCreationForm()

    if request.method == 'POST': 
        form= UserCreationForm(request.POST)

        if form.is_valid():
            user= form.save(commit= False) #creates form and also commit= False saves user to an obj
            user.username= user.username.lower()
            user.save()

            login(request, user)
            return redirect('forums') # CHANGE TO HOMEPAGE
        else:
            messages.error(request, 'An error occurred during registration.')
        


    context= {'form': form}  
    return render(request, 'counter/login_register.html', context)






def home(request):
    return render(request, 'counter/home.html')



#homepage req
def foodcalc(request): 
    import requests 
    import json 

    if request.method == 'POST': #when someone searches for a food, takes the req to process
        query= request.POST['query']
        api_url= 'https://api.api-ninjas.com/v1/nutrition?query=' + query 
        api_request=requests.get(api_url , headers= {'X-Api-Key': 'u5vq9UaMtsQa6ItWSEISiA==jJ9dmq2jaz4bkpXV'}) #sends get req to apininjas to get the nutritional info

        try:
            api= json.loads(api_request.content)[0] #Processes the content received from API and converts it to a python object
            api["serving"]= '100g ' + api["name"] # setting serving size to default 100g
            api["name"]= query
            
            if re.search("\d", query): #it is a valid food and the input has a # it means there is a custom serving size so we adjust
                api["serving"]= query
        except Exception as e: #input not recognized by api, ie. not a food 
                api = "Error"
                print(e)
        return render(request, 'counter/foodcalc.html', {'api': api})
    else:
        return render(request, 'counter/foodcalc.html', {'query': 'Enter a valid query'})
    

#tdee calc
def tdee(request):
    result= 0
    form= TDEEForm()

    activity= {'none': 1, 'sedentary': 1.2, 'light': 1.375, 'moderate': 1.55, 'active': 1.725}

    if request.method == 'POST':
        form= TDEEForm(request.POST) 

        if form.is_valid(): #calculate result
            age = form.cleaned_data['age']
            sex = form.cleaned_data['sex']
            weight = form.cleaned_data['weight'] / 2.2 #convert to kg
            height = form.cleaned_data['height'] * 2.54 # convert to cm
            activity_lvl = activity[form.cleaned_data['activity_lvl']]

            sex_diff= -161 #set to calculate difference in sex
            if sex == 'male':
                sex_diff= 5

            result= 10 * weight + 6.25 * height - 5 * age + sex_diff
            result *= activity_lvl

    
    context= {'form': form, 'result': result}

    return render(request, 'counter/tdee.html', context)







def forums(request):
    q= request.GET.get('q') if request.GET.get('q') != None else '' #get the topic, if no topic then it should be blank

    # icontains, returns objects that at least contain q, so if q is blank everything will show
    rooms= Room.objects.filter( 
        Q(topic__name__icontains= q) | 
        Q(name__icontains= q) | 
        Q(description__icontains= q) 
        ) 
    
    room_count= rooms.count() #faster then python len() method
    room_messages= Message.objects.filter(Q(room__topic__name__icontains=q)) # modify here if you want to filter activity feed
    topics= Topic.objects.all()

    context= {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'counter/forums.html', context)




def room(request, pk):
    room= Room.objects.get(id= pk) # Tables automatically have an id for each instance, queries database looks for matching id and gets obj
    room_messages= room.message_set.all()
    participants= room.participants.all()

    if request.method == 'POST':
        message= Message.objects.create(
            user=request.user, 
            room= room, 
            body= request.POST.get('body')
            )
        
        room.participants.add(request.user)
        return redirect('room', pk= room.id)

    context= {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'counter/room.html', context)



def userProfile(request, pk):
    user= User.objects.get(id= pk)
    rooms= user.room_set.all()
    room_messages= user.message_set.all()
    topics= Topic.objects.all()

    context= {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'counter/profile.html', context)







@login_required(login_url= 'login')
def createRoom(request):
    form= RoomForm()
    topics= Topic.objects.all()

    if request.method == 'POST':
        topic_name= request.POST.get('topic')
        topic, created= Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host= request.user,
            topic= topic,
            name= request.POST.get('name'),
            description= request.POST.get('description')
        )
        #form = RoomForm(request.POST) # passes in data from POST into the form
        #if form.is_valid():
           # room= form.save(commit= False) # saves model in the database
           # room.host= request.user
           # room.save()
            
        return redirect('forums')

    context={'form': form, 'topics':topics}
    return render(request, 'counter/room_form.html', context)



@login_required(login_url= 'login')
def updateRoom(request, pk):
    room= Room.objects.get(id= pk)
    form= RoomForm(instance= room) #pre-fills form with the values from a given room
    topics= Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You do not have permission to update this room.')
    
    if request.method == 'POST':
        topic_name= request.POST.get('topic')
        topic, created= Topic.objects.get_or_create(name=topic_name)

        room.name= request.POST.get('name')        
        room.topic= topic
        room.description= request.POST.get('description')   
        room.save()     


        return redirect('forums')

    context= {'form': form, 'topics': topics, 'room': room}
    return render(request, 'counter/room_form.html', context)



@login_required(login_url= 'login')
def deleteRoom(request, pk):
    room= Room.objects.get(id= pk)

    if request.user != room.host:
        return HttpResponse('You do not have permission to delete this room.')

    if request.method == 'POST':
        room.delete()
        return redirect('forums')
    
    return render(request, 'counter/delete.html', {'obj': room})

@login_required(login_url= 'login')
def deleteMessage(request, pk):
    message= Message.objects.get(id= pk)

    if request.user != message.user:
        return HttpResponse('You do not have permission to delete this message.')

    if request.method == 'POST':
        message.delete()
        return redirect('forums')
    
    return render(request, 'counter/delete.html', {'obj': message})

