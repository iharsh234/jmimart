from django.shortcuts import render
from .forms import StudentForm, UserForm
from .models import User, Student, Item
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.core.urlresolvers import reverse
from django.utils.html import escape
from random import randint
from django.core.mail import send_mail

# Create your views here.

@login_required
def index(request):
    user = request.user
    student = Student.objects.filter(user=user).get()
    items = Item.objects.filter(student=student).order_by('-timestamp')[:3]
    context_dict = {
        'user': user,
        'student': student,
        'items': items,
    }
    return render(request, 'users/index.html', context_dict)

def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/users')
    if request.method == 'POST':
        email = escape(request.POST.get('email').strip())
        user = User.objects.filter(email=email)
        if user:
            user = user.get()
            username = user.username
            password = escape(request.POST.get('password').strip())
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/users')
                else:
                    return HttpResponse('Your account is disabled')
            else:
                login_form = StudentForm(request.POST)
                login_form.add_error('email', 'Invalid login details')
                return render(request, 'users/login.html', {'login_form': login_form})
        else:
            login_form = StudentForm(request.POST)
            login_form.add_error('email', 'Email ID does not exist. Please register')
            return render(request, 'users/login.html', {'login_form': login_form})
    else:
        return render(request, 'users/login.html', {})

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/users')
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
                return HttpResponseRedirect('/users')
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

    return render(request, 'users/register.html', context_dict)

@login_required
def profile(request):
    user = User.objects.get(username=request.user.username)
    student = Student.objects.get(user=user)
    context_dict = {
        'user': user,
        'student': student,
    }

    if request.method == 'POST':
        first_name = escape(request.POST.get('first_name').strip())
        last_name = escape(request.POST.get('last_name').strip())
        mobile = escape(request.POST.get('mobile').strip())
        if request.POST.get('newsletter') == 'on':
            newsletter = True
        else:
            newsletter = False
        User.objects.filter(username=request.user.username).update(first_name=first_name, last_name=last_name)
        Student.objects.filter(user=user).update(mobile=mobile, newsletter=newsletter)
        return HttpResponseRedirect(reverse('user:profile'))
    else:
        return render(request, 'users/profile.html', context_dict)

@login_required
def change_password(request):
    context_dict = {}
    if request.method == 'POST':
        user = request.user
        username = user.username
        current = escape(request.POST.get('current_password'))
        password = escape(request.POST.get('password'))
        retype = escape(request.POST.get('retype_password'))
        auth = authenticate(username=user.username, password=current)
        if auth is None:
            context_dict['wrong_password'] = True
        elif password != retype:
            context_dict['not_same'] = True
        else:
            user.set_password(password)
            user.save()
            logout(request);
            user = authenticate(username=username, password=password)
            login(request, user)
            context_dict['password_changed'] = True

    return render(request, 'users/change_password.html', context_dict)

def forgot_password(request):
    context_dict = {}
    if request.method == 'POST':
        email = escape(request.POST.get('email').strip())
        user = User.objects.filter(email=email)
        if user:
            user = user.get()
            username = user.username
            box = ['Q', '$', 'B', '#', 'W', '@', 'L', 'A']
            rpass = box[randint(0, 7)] + box[randint(0, 7)] + box[randint(0, 7)] + box[randint(0, 7)] + box[randint(0, 7)]
            print username
            print rpass
            print type(rpass)
            user.set_password(rpass)
            user.save()
            message = 'Dear ' + username + '\nYour new password is: ' + rpass
            message += '\nKindly change the password once you log in through the password provided above.'
            message += '\n\n Regards!\nJMImart'
            send_mail("JMIMART - Password Reset", message, 'jmimart.zishan@gmail.com', [email], fail_silently=False)
            context_dict['sent_mail'] = True
        else:
            context_dict['invalid_user'] = True

    return render(request, 'users/forgot_password.html', context_dict)

@login_required
def new(request):
    from uuid import uuid4

    if request.method == 'POST':
        student = Student.objects.get(user=request.user)
        image = request.FILES.get('image')
        item_type = escape(request.POST.get('item_type'))
        title = escape(request.POST.get('title').strip())
        author = escape(request.POST.get('author').strip())
        publisher = escape(request.POST.get('publisher').strip())
        price = escape(request.POST.get('price').strip())
        description = escape(request.POST.get('description').strip())
        condition = escape(request.POST.get('condition').strip())
        image.name = '{}{}'.format(uuid4().hex, image.name[image.name.rfind('.'):])
        item = Item(title=title, author=author, publisher=publisher, price=price, description=description,
                    image=image, item_type=item_type, student=student, sold=False, condition=condition)
        item.save()
        student.item_count += 1
        student.save()
        return HttpResponseRedirect(reverse('user:index'))
    return render(request, 'users/new.html', {})

def sold(request, id):
    student = Student.objects.get(user=request.user)
    Item.objects.filter(student=student, id=id).update(sold=True)
    return HttpResponseRedirect('/users/item/'+id)

@login_required
def edit(request, id):
    student = Student.objects.get(user=request.user)
    item = Item.objects.get(student=student, id=id)
    context_dict = {
        'student': student,
        'item': item,
    }
    return render(request, 'users/edit.html', context_dict)

@login_required
def save(request):
    if request.method == 'POST':
        student = Student.objects.get(user=request.user)
        item_type = request.POST.get('item_type')
        title = escape(request.POST.get('title').strip())
        author = escape(request.POST.get('author').strip())
        publisher = escape(request.POST.get('publisher').strip())
        price = escape(request.POST.get('price').strip())
        description = escape(request.POST.get('description').strip())
        condition = escape(request.POST.get('condition').strip())
        id = request.POST.get('id')
        Item.objects.filter(student=student, id=id).update(item_type=item_type,
                                                           title=title,
                                                           author=author,
                                                           publisher=publisher,
                                                           price=price,
                                                           description=description,
                                                           condition=condition)
        return HttpResponseRedirect('/users/item/'+id)

@login_required
def view(request):
    student = Student.objects.get(user=request.user)
    items = Item.objects.filter(student=student).order_by('-timestamp')
    context_dict = {
        'items': items,
    }
    return render(request, 'users/view.html', context_dict)

@login_required
def item(request, id):
    student = Student.objects.get(user=request.user)
    single_item = Item.objects.filter(student=student).get(id=id)
    context_dict = {
        'id': id,
        'item': single_item,
        'student': student,
    }
    return render(request, 'users/item.html', context_dict)

@login_required
def delete_item(request, id):
    student = Student.objects.get(user=request.user)
    Item.objects.filter(student=student, id=id).delete()
    return HttpResponseRedirect(reverse('user:view'))

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')