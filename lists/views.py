from django.http import HttpResponse
from django.shortcuts import render, redirect
from lists.models import Item

# Create your views here.
def home_page(request):
    '''Домашняя страница'''
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    items = Item.objects.all()

    # item = Item()
    # item.text = request.POST.get('item_text', '')
    # item.save()
    return render(request, 'home.html', {'items': items})

