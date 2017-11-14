from django import forms


class UploadPicForm(forms.Form):
      poster = forms.CharField(label='Jouw naam, echt of vals', max_length=255)
      file = forms.ImageField(label='Een mooie foto')
