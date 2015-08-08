from django.shortcuts import render
from django.http import HttpResponse
from users.models import Item, Student, Views
from datetime import datetime
from django.utils.html import escape
from django.core.mail import send_mail

# Create your views here.

def index(request):
    books = Item.objects.filter(item_type='book').order_by('-timestamp')[:8]
    stationary = Item.objects.filter(item_type='stationary').order_by('-timestamp')[:8]
    others = Item.objects.filter(item_type='others').order_by('-timestamp')[:8]
    context_dict = {
        'books': books,
        'stationary': stationary,
        'others': others,
    }
    return render(request, 'index.html', context_dict)

def item(request, id):
    single_item = Item.objects.get(id=id)
    student = Student.objects.get(id=single_item.student_id)
    item_views = Views.objects.filter(item=single_item, student=student)
    if item_views:
        count = item_views.get().count
        item_views.update(count=count+1,
                          datetime=datetime.now())
    else:
        item_view = Views(item=single_item, student=student, count=1)
        item_view.save()
    context_dict = {
        'item': single_item,
        'student': student,
    }
    return render(request, 'item.html', context_dict)

def books(request, p):
    if not p:
        p = 1
    p = int(p)
    many_books = Item.objects.filter(item_type='book').order_by('-timestamp')[12*(p-1):12*p]
    return render(request, 'books.html', {'books': many_books, 'next': p+1, 'prev': p-1})

def stationary(request, p):
    if not p:
        p = 1
    p = int(p)
    many_stationary = Item.objects.filter(item_type='stationary').order_by('-timestamp')[12*(p-1):12*p]
    return render(request, 'stationary.html', {'stationary': many_stationary, 'next': p+1, 'prev': p-1})

def others(request, p):
    if not p:
        p = 1
    p = int(p)
    many_others = Item.objects.filter(item_type='others').order_by('-timestamp')[12*(p-1):12*p]
    return render(request, 'others.html', {'others': many_others, 'next': p+1, 'prev': p-1})

def search(request):
    if request.method == 'POST':
        q = escape(request.POST.get('search').strip())
        items = Item.objects.filter(title__icontains=q)
        return render(request, 'search.html', {'items': items})


def tnc(request):
    return render(request, 'tnc.html', {})

def contact(request):
    context_dict = {}
    if request.method == 'POST':
        name = escape(request.POST.get('name').strip())
        email = escape(request.POST.get('email').strip())
        message = escape(request.POST.get('message').strip())
        message += '\nEmail: ' + email
        send_mail("JMIMART - Contact: " + name, message, email, ['zishanrbp@gmail.com'], fail_silently=False)
        context_dict['sent'] = True

    return render(request, 'contact.html', context_dict)

def howto(request):
    return render(request, 'howto.html', {})

def ambassador(request):
    return render(request, 'ambassador.html', {})