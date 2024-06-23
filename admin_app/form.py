from django.forms import ModelForm

from .models import CategoryInfoModel

class CategoryForm(ModelForm):
    
    class Meta:
        model=CategoryInfoModel
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['categoryhomeimage'].required = False
        self.fields['categorysectionimage'].required = False