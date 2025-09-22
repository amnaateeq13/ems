from django import forms
from users.models import User
from .models import ParentProfile

from django import forms
from users.models import User
from .models import ParentProfile

from django import forms
from users.models import User
from .models import ParentProfile

class ParentUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data




class ParentProfileForm(forms.ModelForm):
    class Meta:
        model = ParentProfile
        fields = ['contact_number', 'children']  # parent_id will be auto


from django import forms
from .models import ParentProfile

class ParentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = ParentProfile
        fields = ['contact_number', 'address', 'profile_picture']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
