from django import forms


class UploadPicForm(forms.Form):
      poster = forms.CharField(label='Jouw naam, echt of vals', max_length=255)
      file = forms.ImageField(label='Een mooie foto')


class UploadAdForm(forms.Form):
      poster = forms.CharField(label='De WG of PG of reclameerder', max_length=255)
      file = forms.ImageField(label='Reklam')
