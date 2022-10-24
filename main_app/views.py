from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect

from .models import Vaca, Stuff, Photo

from django.contrib.auth import login

from .forms import TravelingForm

from django.contrib.auth.forms import UserCreationForm

import boto3
import uuid

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'cat-collector-photo-upload-29'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def vacas_index(request): 
    vacas = Vaca.objects.all()
    return render(request, 'vacas/index.html', {'vacas' : vacas})

@login_required
def vacas_detail(request, vaca_id):
    vaca = Vaca.objects.get(id=vaca_id)
    traveling_form = TravelingForm()
    stuffs = Stuff.objects.exclude(id__in=vaca.stuffs.all().values_list('id'))
    return render(request, 'vacas/detail.html', {
        'vaca': vaca,
        'traveling_form' : traveling_form,
        'stuffs' : stuffs
        })

@login_required
def add_traveling(request, vaca_id):
    print(request.POST)
    form= TravelingForm(request.POST)
    if form.is_valid():
        new_traveling = form.save(commit=False)
        new_traveling.vaca_id = vaca_id
        new_traveling.save()
    else:
        print(form.errors)
    return redirect('vacas_detail', vaca_id=vaca_id)

@login_required
def assoc_stuff(request, vaca_id, stuff_id):
    Vaca.objects.get(id=vaca_id).stuffs.add(stuff_id)
    return redirect('vacas_detail', vaca_id=vaca_id)


@login_required
def add_photo(request, vaca_id):
    photo_file = request.FILES.get('photo-files')
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f'{S3_BASE_URL}{BUCKET}/{key}'
            photo = Photo(url=url, vaca_id=vaca_id)
            photo.save()
        except Exception as error:
            print('An error has occured uploading or saving the new photo')
            print(error)
    return redirect('vacas_detail', vaca_id=vaca_id)


def signup(request):
    error_message = None
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('vacas_index')
        else:
            error_message = 'Signup input invalid - Please try again'
    form = UserCreationForm()
    context = { 'form': form, 'error': error_message }
    return render(request, 'registration/signup.html', context)

class VacasCreate(LoginRequiredMixin, CreateView):
    model = Vaca
    fields = ('name', 'location', 'city', 'description', 'cost')

class VacasUpdate (LoginRequiredMixin, UpdateView):
    model = Vaca
    fields = ('description', 'cost')

class VacasDelete(LoginRequiredMixin, DeleteView):
    model = Vaca
    success_url = '/vacas/'

class StuffsCreate(LoginRequiredMixin, CreateView):
    model = Stuff
    fields = ('name', 'description')

class StuffsIndex(LoginRequiredMixin, ListView):
    template_name = 'stuffs/index.html'
    model = Stuff

class StuffsDetail(LoginRequiredMixin, DetailView):
    template_name = 'stuffs/detail.html'
    model = Stuff

class StuffsUpdate(LoginRequiredMixin, UpdateView):
    model = Stuff
    fields = ('name', 'description')

class StuffsDelete(LoginRequiredMixin, DeleteView):
    model = Stuff
    success_url = '/stuffs/'
