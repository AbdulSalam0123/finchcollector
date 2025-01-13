from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Finch, Toy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import FeedingForm


class FinchCreate(CreateView):
    model = Finch
    fields =['name', 'type', 'description', 'age']

class FinchUpdate(UpdateView):
    model = Finch
    fields = ['type', 'description', 'age', 'image']

class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches/'

class ToyList(ListView):
    model = Toy

class ToyDetail(DetailView):
    model = Toy

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def finches_index(request):
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', {'finches': finches})

def finch_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    feeding_form = FeedingForm()
    # exclude those toys ids which exists in the finches_toys joint table with the current finch id
    # remaining toys ids will be returned to toys_finch_doesn't_have
    toys_finch_doesnt_have = Toy.objects.exclude(id__in = finch.toys.all().values_list('id'))
    return render(request, 'finches/detail.html' , {'finch': finch, 'feeding_form': feeding_form, 'toys': toys_finch_doesnt_have})

def add_feeding(request, finch_id):
    form = FeedingForm(request.POST)
    if(form.is_valid):
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect('detail', finch_id=finch_id)

def assoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect('detail', finch_id = finch_id)

def unassoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.remove(toy_id)
    return redirect('detail', finch_id = finch_id)
    

    