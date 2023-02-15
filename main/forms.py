from django import forms
from .models import OwnerModel

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()

class ObjectForm(forms.ModelForm):
    class Meta:
        model = OwnerModel
        fields = ['lexemm', 'morph', 'role', ]

        widgets = {
            "lexemm": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Лексемма'
            }),
            'morph': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Морф разбор'
            }),
            'role': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Роль в предложении'
            }),
        }
