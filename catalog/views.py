from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import DesignRequest, Category
from .forms import RegisterForm, RequestForm, AcceptRequestForm, CompleteRequestForm, CategoryForm



def index(request):
    completed_requests = DesignRequest.objects.filter(
        status='completed'
    )[:4]

    accepted_count = DesignRequest.objects.filter(
        status='accepted'
    ).count()

    return render(request, 'index.html', {
        'completed_requests': completed_requests,
        'accepted_count': accepted_count
    })


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('account')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    error = ''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect('superadmin')

            return redirect('account')
        else:
            error = 'Неверный логин или пароль.'

    return render(request, 'login.html', {'error': error})


@login_required(login_url='login')
def account(request):
    user_requests = request.user.design_requests.all()

    selected_status = request.GET.get('status', '')

    if selected_status in ['new', 'accepted', 'completed']:
        user_requests = user_requests.filter(status=selected_status)

    return render(request, 'account.html', {
        'user_requests': user_requests,
        'selected_status': selected_status
    })


@login_required(login_url='login')
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)

        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.user = request.user
            new_request.save()

            messages.success(request, 'Заявка успешно создана.')
            return redirect('account')
    else:
        form = RequestForm()

    return render(request, 'request_create.html', {'form': form})


def user_logout(request):
    if request.method == 'POST':
        logout(request)

    return redirect('index')


@login_required(login_url='login')
def delete_request(request, request_id):
    design_request = get_object_or_404(
        DesignRequest,
        id=request_id,
        user=request.user
    )

    if request.method == 'POST':
        if design_request.status == 'new':
            design_request.delete()
            messages.success(request, 'Заявка успешно удалена.')
        else:
            messages.error(
                request,
                'Нельзя удалить заявку, статус которой уже изменён.'
            )

    return redirect('account')


@staff_member_required(login_url='login')
def superadmin(request):
    all_requests = DesignRequest.objects.all()
    categories = Category.objects.all()
    category_form = CategoryForm()

    return render(request, 'superadmin.html', {
        'all_requests': all_requests,
        'categories': categories,
        'category_form': category_form
    })


@staff_member_required(login_url='login')
def accept_request(request, request_id):
    design_request = get_object_or_404(
        DesignRequest,
        id=request_id,
        status='new'
    )

    if request.method == 'POST':
        form = AcceptRequestForm(
            request.POST,
            instance=design_request
        )

        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.status = 'accepted'
            design_request.save()

            messages.success(
                request,
                'Заявка принята в работу.'
            )
        else:
            messages.error(
                request,
                'Для принятия заявки необходимо указать комментарий.'
            )

    return redirect('superadmin')


@staff_member_required(login_url='login')
def complete_request(request, request_id):
    design_request = get_object_or_404(
        DesignRequest,
        id=request_id,
        status='new'
    )

    if request.method == 'POST':
        form = CompleteRequestForm(
            request.POST,
            request.FILES,
            instance=design_request
        )

        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.status = 'completed'
            design_request.save()

            messages.success(
                request,
                'Заявка отмечена как выполненная.'
            )
        else:
            messages.error(
                request,
                'Необходимо загрузить изображение готового дизайна.'
            )

    return redirect('superadmin')

@staff_member_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно добавлена.')
        else:
            messages.error(request, 'Не удалось добавить категорию.')

    return redirect('superadmin')


@staff_member_required(login_url='login')
def delete_category(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(
            Category,
            id=category_id
        )
        category.delete()
        messages.success(
            request,
            'Категория и связанные с ней заявки удалены.'
        )

    return redirect('superadmin')
