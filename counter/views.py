from django.shortcuts import render
from.tdeeform import TDEEForm

# Create your views here.

#API KEY: u5vq9UaMtsQa6ItWSEISiA==jJ9dmq2jaz4bkpXV

#homepage req
def foodcalc(request): 
    import requests 
    import json 

    if request.method == 'POST': #when someone searches for a food, takes the req to process
        query= request.POST['query']
        api_url= 'https://api.api-ninjas.com/v1/nutrition?query=' + query 
        api_request=requests.get(api_url , headers= {'X-Api-Key': 'u5vq9UaMtsQa6ItWSEISiA==jJ9dmq2jaz4bkpXV'}) #sends get req to apininjas to get the nutritional info

        try:
            api= json.loads(api_request.content) #Processes the content received from API and converts it to a python object
        except Exception as e:
                api = "Error"
                print(e)
        return render(request, 'foodcalc.html', {'api': api})
    else:
        return render(request, 'foodcalc.html', {'query': 'Enter a valid query'})
    

def tdee(request):
    if request.method == 'POST':
        form= TDEEForm(request.POST) 
        if form.is_valid():
            result=0
            

    else:
        form= TDEEForm()
        result= 0

    return render(request, 'tdee.html', {'form': form, 'result': result})
