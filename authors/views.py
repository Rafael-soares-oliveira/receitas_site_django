from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
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
        return render(request, 'pages/register_created.html')

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
            login(request, authenticated_user)
            return render(request, 'pages/dashboard.html')
        else:
            messages.error(request, 'Username or password incorrect!')
    else:
        messages.error(request, 'Invalid username or password')

    return redirect(login_url)


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))
    else:
        logout(request)
        return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes_published = Recipe.objects.filter(
        is_published=True,
        author=request.user
    )
    recipes_not_published = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    return render(request, 'pages/dashboard.html', context={
        'recipes_published': recipes_published,
        'recipes_not_published': recipes_not_published,
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    )

    if not recipe:
        raise Http404()

    return render(request, 'pages/dashboard_recipe.html', context={
        'recipe': recipe
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def recipe_not_published(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=False)
    return render(request, 'pages/recipe-view.html',
                  context={
                      'recipe': recipe,
                  })
