from django.shortcuts import redirect, render, get_object_or_404
from authors.forms_recipe import AuthorsRecipeForm
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
            return render(request, 'pages/login.html')
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
def recipe_not_published(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=False)
    return render(request, 'pages/recipe-view.html',
                  context={
                      'recipe': recipe,
                  })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.get(
        is_published=False,
        author=request.user,
        pk=id,
    )

    form = AuthorsRecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe,
    )

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_step_is_html = False
        recipe.is_published = False
        recipe.save()

        messages.success(request, 'Your recipe has been saved sucessfully!')
        return render(request, 'pages/recipe-view.html',
                      context={
                          'recipe': recipe,
                      })

    return render(request, 'pages/dashboard_recipe_edit.html', context={
        'recipe': recipe,
        'form': form
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_create(request):
    form = AuthorsRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe: Recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_step_is_html = False
        recipe.is_published = False
        recipe.save()

        messages.success(request, 'Your recipe has been created sucessfully!')
        return redirect(
            reverse('authors:dashboard_recipe_edit',
                    args=[recipe.id]))  # type:ignore

    return render(request, 'pages/dashboard_recipe_edit.html', context={
        'form': form
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()

    if not recipe:
        raise Http404

    recipe.delete()

    messages.warning(request, 'Your recipe has been delete sucessfully!')

    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_unpublish(request, id):
    recipe = Recipe.objects.filter(
        is_published=True,
        author=request.user,
        pk=id,
    ).first()

    if not recipe:
        raise Http404

    recipe.is_published = False
    recipe.save()

    messages.warning(request, 'Your recipe has been unpublished sucessfully!')

    return redirect(reverse('authors:dashboard'))
