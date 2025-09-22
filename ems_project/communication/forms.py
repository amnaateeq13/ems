from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'message', 'audience']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.role == 'teacher':
            self.fields['audience'].choices = [
                ('student', 'Student'),
                ('parent', 'Parent'),
            ]


from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Type your message...', 'class': 'chat-input'}),
        }
