from django import forms

class MainForm(forms.Form):
    address = forms.CharField(max_length=200, label='', widget=forms.TextInput(attrs={
        'placeholder': 'Address',
        'class' : 'form-control'
    }))
    search_query = forms.CharField(max_length=50, label='', widget=forms.TextInput(attrs={
        'placeholder': 'Search',
        'class' : 'form-control'
    }))

