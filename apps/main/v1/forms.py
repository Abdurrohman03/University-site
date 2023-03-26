from django import forms
from apps.main.models import Subscribe, Contact


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control email',
            'placeholder': 'Enter email',
            'autocomplete': 'off'
        })


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'type': 'text',
            'id': 'name',
            'class': 'form-control py-2'
        })
        self.fields['email'].widget.attrs.update({
            'type': 'email',
            'id': 'email',
            'class': 'form-control py-2'
        })
        self.fields['body'].widget.attrs.update({
            'type': 'message',
            'id': 'message',
            'class': 'form-control py-2',
            'cols': '30',
            'rows': '8'
        })

