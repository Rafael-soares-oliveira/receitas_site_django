from django.shortcuts import redirect, render
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
# Create your views here.


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    request.session['register_form_data'] = request.POST
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in.')
        return redirect('authors:home')
    else:
        messages.error(request, 'Please fix.')

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    login_url = reverse('authors:login')

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Your are logged in.')
            login(request, authenticated_user)
            return redirect(reverse('authors:home'))
        else:
            messages.error(request, 'Username or password incorrect!')
    else:
        messages.error(request, 'Invalid username or password')

    return redirect(login_url)


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    logout(request)
    return redirect(reverse('authors:home'))
