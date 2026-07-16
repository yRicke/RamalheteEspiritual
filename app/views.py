import json
from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Sum
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date

from .models import Ramalhete


PRACTICE_FIELDS = (
    'missa_comunhao',
    'visita_ao_santissimo',
    'tercos',
    'exame_de_consciencia',
    'leitura_espiritual_meditacao',
    'sacrificio',
)


def superuser_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return login_required(wrapped_view, login_url='entrar')


def get_totals(queryset):
    totals = queryset.aggregate(**{
        field: Sum(field)
        for field in PRACTICE_FIELDS
    })
    return {
        field: totals[field] or 0
        for field in PRACTICE_FIELDS
    }


def home(request):
    if request.user.is_superuser:
        usuarios = User.objects.filter(is_superuser=False).order_by('username')
        return render(request, 'admin_home.html', {'usuarios': usuarios})

    status_por_data = {}

    if request.user.is_authenticated:
        ramalhetes = Ramalhete.objects.filter(usuario=request.user).values('data', *PRACTICE_FIELDS)
        for ramalhete in ramalhetes:
            data = ramalhete['data'].isoformat()
            possui_pratica_registrada = any(ramalhete[campo] != 0 for campo in PRACTICE_FIELDS)
            status_por_data[data] = 'complete' if possui_pratica_registrada else 'pending'

    return render(request, 'home.html', {'status_por_data': json.dumps(status_por_data)})


def entrar(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        return render(request, 'entrar.html', {'error': 'Credenciais invalidas'})
    return render(request, 'entrar.html')


def sair(request):
    logout(request)
    return redirect('home')


@login_required(login_url='entrar')
def abrir_ramalhate(request, data):
    data_ramalhete = parse_date(data)
    if data_ramalhete is None:
        raise Http404("Data invalida")

    ramalhete, _ = Ramalhete.objects.get_or_create(
        usuario=request.user,
        data=data_ramalhete,
        defaults={
            'missa_comunhao': 0,
            'visita_ao_santissimo': 0,
            'tercos': 0,
            'exame_de_consciencia': 0,
            'leitura_espiritual_meditacao': 0,
            'sacrificio': 0,
        }
    )
    return render(request, 'ramalhete.html', {'ramalhete': ramalhete})


@login_required(login_url='entrar')
def resumo_mensal(request, ano, mes):
    if not 1900 <= ano <= 2200 or not 1 <= mes <= 12:
        raise Http404("Periodo invalido")

    ramalhetes = Ramalhete.objects.filter(
        usuario=request.user,
        data__year=ano,
        data__month=mes,
    )
    return JsonResponse(get_totals(ramalhetes))


@superuser_required
def resumo_admin_mensal(request, ano, mes):
    if not 1900 <= ano <= 2200 or not 1 <= mes <= 12:
        raise Http404("Periodo invalido")

    ramalhetes = Ramalhete.objects.filter(
        usuario__is_superuser=False,
        data__year=ano,
        data__month=mes,
    )
    return JsonResponse(get_totals(ramalhetes))


@superuser_required
def criar_usuario(request):
    if request.method != 'POST':
        return redirect('home')

    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')

    if not username or not password:
        messages.error(request, 'Informe o nome de usuario e a senha.')
        return redirect('home')

    if User.objects.filter(username__iexact=username).exists():
        messages.error(request, 'Ja existe um usuario com esse nome.')
        return redirect('home')

    usuario = User(username=username)
    try:
        validate_password(password, usuario)
    except ValidationError as error:
        messages.error(request, ' '.join(error.messages))
        return redirect('home')

    usuario.set_password(password)
    usuario.save()
    messages.success(request, f'Usuario {username} criado com sucesso.')
    return redirect('home')


@superuser_required
def editar_usuario(request, usuario_id):
    if request.method != 'POST':
        return redirect('home')

    usuario = get_object_or_404(User, id=usuario_id, is_superuser=False)
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')
    is_active = request.POST.get('is_active') == 'on'

    if not username:
        messages.error(request, 'O nome de usuario nao pode ficar vazio.')
        return redirect('home')

    if User.objects.filter(username__iexact=username).exclude(id=usuario.id).exists():
        messages.error(request, 'Ja existe um usuario com esse nome.')
        return redirect('home')

    if password:
        try:
            validate_password(password, usuario)
        except ValidationError as error:
            messages.error(request, ' '.join(error.messages))
            return redirect('home')
        usuario.set_password(password)

    usuario.username = username
    usuario.is_active = is_active
    usuario.save()
    messages.success(request, f'Usuario {username} atualizado.')
    return redirect('home')


@login_required(login_url='entrar')
def editar_ramalhete(request, data):
    data_ramalhete = parse_date(data)
    if data_ramalhete is None:
        raise Http404("Data invalida")

    if request.method != 'POST':
        return JsonResponse({'erro': 'Metodo nao permitido.'}, status=405)

    campo = request.POST.get('campo')

    if campo not in PRACTICE_FIELDS:
        return JsonResponse({'erro': 'Campo invalido.'}, status=400)

    try:
        valor = int(request.POST.get('valor', 0))
    except (TypeError, ValueError):
        return JsonResponse({'erro': 'Valor invalido.'}, status=400)

    if valor < 0:
        return JsonResponse({'erro': 'O valor nao pode ser negativo.'}, status=400)

    ramalhete = Ramalhete.objects.get(usuario=request.user, data=data_ramalhete)
    setattr(ramalhete, campo, valor)
    ramalhete.save(update_fields=[campo])
    return JsonResponse({'campo': campo, 'valor': valor})
