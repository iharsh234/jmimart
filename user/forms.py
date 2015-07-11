from django import forms
from django.contrib.auth.models import User


class StudentForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def clean(self):
        cleaned_data = super(StudentForm, self).clean()
        email = cleaned_data.get("email")
        if email and User.objects.filter(email=email).count():
            self.add_error('email', 'Email ID exists')