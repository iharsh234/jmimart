from django.shortcuts import render
from .forms import StudentForm, UserForm
from .models import User, Student
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.core.urlresolvers import reverse

# Create your views here.

@login_required
def index(request):
    user = request.user
    student = Student.objects.filter(user=user).get()
    context_dict = {
        'user': user,
        'student': student,
    }
    return render(request, 'user/index.html', context_dict)

def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/user')
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email)
        if user:
            user = user.get()
            username = user.username
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user')
                else:
                    return HttpResponse('Your account is disabled')
            else:
                login_form = StudentForm(request.POST)
                login_form.add_error('email', 'Invalid login details')
                return render(request, 'user/login.html', {'login_form': login_form})
        else:
            login_form = StudentForm(request.POST)
            login_form.add_error('email', 'Email ID does not exist. Please register')
            return render(request, 'user/login.html', {'login_form': login_form})
    else:
        return render(request, 'user/login.html', {})

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/user')
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        user_form = UserForm(request.POST)
        if request.POST.get('password') == request.POST.get('confirm_password'):
            if student_form.is_valid() and user_form.is_valid():
                user = student_form.save()
                user.set_password(user.password)
                user.save()
                student = user_form.save(commit=False)
                student.user = user
                if request.POST.get('checked'):
                    student.newsletter = 1
                else:
                    student.newsletter = 0
                student.item_count = 0
                student.save()
                user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
                login(request, user)
                return HttpResponseRedirect('/user')
            else:
                print(student_form.errors)
                print(user_form.errors)
        else:
            student_form.add_error('password', 'Passwords do not match. Enter again')
    else:
        student_form = StudentForm()

    context_dict = {
        'student_form': student_form,
    }

    return render(request, 'user/register.html', context_dict)

def profile(request):
    user = User.objects.get(username=request.user.username)
    student = Student.objects.get(user=user)
    context_dict = {
        'user': user,
        'student': student,
    }

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        if request.POST.get('newsletter') == 'on':
            newsletter = True
        else:
            newsletter = False
        User.objects.filter(username=request.user.username).update(first_name=first_name, last_name=last_name)
        Student.objects.filter(user=user).update(mobile=mobile, newsletter=newsletter)
        user = User.objects.get(username=request.user.username)
        student = Student.objects.get(user=user)
        # context_dict = {
        #     'user': user,
        #     'student': student,
        #     'profile_updated': True
        # }
        # return render(request, 'user/profile.html', context_dict)
        return HttpResponseRedirect(reverse('user:profile'))
    else:
        return render(request, 'user/profile.html', context_dict)


def new(request):
    return render(request, 'user/new.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')