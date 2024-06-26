

from .models import ParentSectionModel
from django import forms
 
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