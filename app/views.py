from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Ramalhete
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'home.html')

def entrar(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'entrar.html', {'error': 'Credenciais inválidas'})
    return render(request, 'entrar.html')

def sair(request):
    logout(request)
    return redirect('home')

def registrar(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'registrar.html')

@login_required(login_url='entrar')
def abrir_ramalhate(request, data):
    if Ramalhete.objects.filter(usuario=request.user, data=data).exists():
        ramalhete = Ramalhete.objects.get(usuario=request.user, data=data)
    else:
        ramalhete = Ramalhete.objects.create(usuario=request.user, data=data, missa_comunhao=0, visita_ao_santissimo=0, tercos=0, exame_de_consciencia=0, leitura_espiritual_meditacao=0, sacrificio=0)
    return render(request, 'ramalhete.html', {'ramalhete': ramalhete})

@login_required(login_url='entrar')
def editar_ramalhete(request, data):
    if request.method == 'POST':
        ramalhete = Ramalhete.objects.get(usuario=request.user, data=data)
        missa_comunhao = int(request.POST.get('missa_comunhao', 0))
        visita_ao_santissimo = int(request.POST.get('visita_ao_santissimo', 0))
        exame_de_consciencia = int(request.POST.get('exame_de_consciencia', 0))
        leitura_espiritual_meditacao = int(request.POST.get('leitura_espiritual_meditacao', 0))
        sacrificio = int(request.POST.get('sacrificio', 0))
        ramalhete.editar_ramalhete(missa_comunhao, visita_ao_santissimo, exame_de_consciencia, leitura_espiritual_meditacao, sacrificio)
        return redirect('abrir_ramalhate', data=data)
    else:
        ramalhete = Ramalhete.objects.get(usuario=request.user, data=data)
        return render(request, 'editar_ramalhete.html', {'ramalhete': ramalhete})