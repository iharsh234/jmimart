from django.shortcuts import render
from django.http import HttpResponse
from user.models import Item, Student

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
    context_dict = {
        'item': single_item,
        'student': student,
    }
    return render(request, 'item.html', context_dict)

def books(request):
    many_books = Item.objects.filter(item_type='book').order_by('-timestamp')
    return render(request, 'books.html', {'books': many_books})

def stationary(request):
    many_stationary = Item.objects.filter(item_type='stationary').order_by('-timestamp')
    return render(request, 'stationary.html', {'stationary': many_stationary})

def others(request):
    many_others = Item.objects.filter(item_type='others').order_by('-timestamp')
    return render(request, 'others.html', {'others': many_others})