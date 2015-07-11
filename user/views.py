from django.shortcuts import render
from .forms import StudentForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate

# Create your views here.

@login_required
def index(request):
    return HttpResponse('hello')

def user_login(request):
    if request.method == 'POST':

    return render(request, 'user/login.html', {})

def register(request):
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        if request.POST.get('password') == request.POST.get('confirm_password'):
            if student_form.is_valid():
                student = student_form.save(commit=False)
                student.set_password(student.password)
                if request.POST.get('checked') == 1:
                    student.newsletter = 1
                else:
                    student.newsletter = 0
                student.book_count = 1
                student.save()
                user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
                login(request, user)
                return HttpResponseRedirect('user/')
            else:
                print(student_form.errors)
        else:
            student_form.add_error('password', 'Passwords do not match. Enter again')
    else:
        student_form = StudentForm()

    context_dict = {
        'student_form': student_form,
    }

    return render(request, 'user/register.html', context_dict)

@login_required
def logout(request):
    logout(request)
    return HttpResponseRedirect('/')