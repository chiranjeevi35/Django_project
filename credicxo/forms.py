from django import forms
from .models import signup_info

class signup_infoform(forms.ModelForm):
     class Meta:
        db_table = 'userinfo'
        model = signup_info
        fields = '__all__'