from django.forms import ModelForm
from django import forms
from .models import Room


class RoomForm(ModelForm):
    class Meta: #specify the model we want to create a form for (Room Model)
        model= Room

        fields= '__all__' #creates a form based off the fields in the Room model
        exclude= ['host', 'participants']


class TDEEForm(forms.Form):
    age= forms.IntegerField(label='Age:')

    sex= forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')], widget=forms.RadioSelect, label='Sex:')

    weight=forms.IntegerField(label='Weight (lbs):')

    height=forms.IntegerField(label='Height (inches):')
    
    activity_lvl= forms.ChoiceField(choices= [('none','None/(Base Metabolic Rate)'), ('sedentary','Sedentary (Office Job)') ,('light','Light: exercises 1-3 days/week') ,('moderate','Moderate: exercises 4-5 days/week'), ('active', 'Active: exercises 6-7 days/week OR intense exercise 3-4 times/week')], widget=forms.Select, label= 'Activity Level:')

    def check_age(self):
        age = self.cleaned_data.get('age')
        if age < 0:
            raise forms.ValidationError("Age must be a non-negative number.")
        return age

    def check_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight < 0:
            raise forms.ValidationError("Weight must be a non-negative number.")
        return weight

    def check_height(self):
        height = self.cleaned_data.get('height')
        if height < 0:
            raise forms.ValidationError("Height must be a non-negative number.")
        return height
        