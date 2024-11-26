from django import forms

class UploadForm(forms.Form):
    arquivo = forms.FileField(label='Selecione um arquivo .las', required=True)
