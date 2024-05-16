from django.shortcuts import render
from.tdeeform import TDEEForm
import re


# Create your views here.

#API KEY: u5vq9UaMtsQa6ItWSEISiA==jJ9dmq2jaz4bkpXV


# Room IDs:
rooms= [
    {'id': 1, 'name': 'Weight Training' },
    {'id': 2, 'name': 'Sports' },
    {'id': 3, 'name': 'Nutrition' }
]









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
    if request.method == 'POST':
        form= TDEEForm(request.POST) 
        if form.is_valid():
            result=0
            age = form.cleaned_data['age']
            sex = form.cleaned_data['sex']
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            activity_lvl = form.cleaned_data['activity_lvl']

    else:
        form= TDEEForm()
        result= 0

    return render(request, 'counter/tdee.html', {'form': form, 'result': result})



def forums(request):
    context= {'rooms': rooms}
    return render(request, 'counter/forums.html', context)

def room(request, pk):
    room= None

    for r in rooms:
        if r['id'] == int(pk):
            room= r

    context= {'room': room}
    return render(request, 'counter/room.html', context)