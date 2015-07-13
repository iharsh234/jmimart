from django import forms
from django.contrib.auth.models import User
from .models import Student

class StudentForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def clean(self):
        cleaned_data = super(StudentForm, self).clean()
        email = cleaned_data.get("email")
        if email and User.objects.filter(email=email).count():
            self.add_error('email', 'Email ID exists')


class UserForm(forms.ModelForm):
    book_count = forms.IntegerField(required=False)
    last_visited = forms.DateTimeField(required=False)

    class Meta:
        model = Student
        fields = ('mobile', 'book_count', 'last_visited')
