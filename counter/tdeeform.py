from django import forms

class TDEEForm(forms.Form):
    age= forms.IntegerField(label='Age:')

    sex= forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')], widget=forms.RadioSelect, label='Sex:')

    weight=forms.IntegerField(label='Weight (lbs):')

    height= forms.ChoiceField(widget=forms.Select, label= 'Height:')
    
    activity_lvl= forms.ChoiceField(choices= [('none','None/(Base Metabolic Rate)'), ('sedentary','Sedentary (Office Job)') ,('light','Light: exercises 1-3 days/week') ,('moderate','Moderate: exercises 4-5 days/week'), ('active', 'Active: exercises 6-7 days/week OR intense exercise 3-4 times/week')], widget=forms.Select, label= 'Activity Level:')