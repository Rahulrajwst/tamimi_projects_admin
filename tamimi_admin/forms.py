

from .models import ParentSectionModel,DeviceOrderModel
from django import forms
from django. contrib.auth.forms import UserCreationForm
from django. contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
 
# define the class of a form
class ParentForm(forms.ModelForm):
    class Meta:
        # write the name of models for which the form is made
        model = ParentSectionModel         
        fields = ['parentsectionname','parentsectionimage']

    def __init__(self, *args, **kwargs):
        super(ParentForm, self).__init__(*args, **kwargs)
        self.fields['parentsectionname'].label = "Name"
        self.fields['parentsectionimage'].label = "Upload image"

    def clean_my_field(self):
        parentsectionname = self.cleaned_data['Name']
        print('testing')
        print(parentsectionname.strip())
        print('end')
        if parentsectionname.strip() == '':
             
            raise forms.ValidationError("This field cannot be empty.")
        return parentsectionname
    
class CreateUserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())