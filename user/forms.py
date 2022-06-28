from django import forms
from user.models import Profile

class ProfileForm(forms.ModelForm):
		class Meta:
				model = Profile
				#fields = ('photo','bio','location','birth_date')
				fields=['photo']
