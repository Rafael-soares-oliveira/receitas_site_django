from django.views import View
from recipes.models import Recipe
from authors.forms_recipe import AuthorsRecipeForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
    )
class DashboardRecipeEdit(View):
    def get_recipe(self, id=None):
        recipe = None
        if id is not None:
            recipe = Recipe.objects.get(
                is_published=False,
                author=self.request.user,
                pk=id,
                )
        return recipe

    def render_recipe(self, recipe, form):
        return render(self.request, 'pages/dashboard_recipe_edit.html',
                      context={
                          'recipe': recipe,
                          'form': form
                          })

    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorsRecipeForm(instance=recipe)
        return self.render_recipe(recipe, form)

    def post(self, request, id=None):
        recipe = self.get_recipe(id)

        form = AuthorsRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe,
        )

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.preparation_step_is_html = False
            recipe.is_published = False
            recipe.save()

            messages.success(
                request, _('Your recipe has been saved sucessfully!'))
            return render(request, 'pages/recipe-view.html',
                          context={
                              'recipe': recipe,
                              })

        return self.render_recipe(recipe, form)


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
    )
class DashboardRecipeDelete(DashboardRecipeEdit):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))
        recipe.delete()  # type:ignore
        messages.warning(
            self.request, _('Your recipe has been delete sucessfully!'))
        return redirect(reverse('authors:dashboard'))


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
    )
class DashboardRecipeUnpublish(DashboardRecipeEdit):
    def get_recipe(self, id):
        recipe = Recipe.objects.get(
            is_published=True,
            author=self.request.user,
            pk=id,
            )
        return recipe

    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))
        recipe.is_published = False
        recipe.save()
        messages.warning(
            self.request, _('Your recipe has been unpublished sucessfully!'))
        return redirect(reverse('authors:dashboard'))


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
    )
class DashboardRecipeUnpublishView(View):
    def get(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id, is_published=False)
        return render(request, 'pages/recipe-view.html',
                      context={
                          'recipe': recipe,
                          })


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
    )
class Dashboard(View):
    def get(self, request):
        recipes_published = self.get_recipe_published(request)
        recipes_not_published = self.get_recipe_not_published(request)
        return self.render_dashboard(request, recipes_published,
                                     recipes_not_published)

    def get_recipe_published(self, request):
        recipes_published = Recipe.objects.filter(
            is_published=True,
            author=request.user
            )

        return recipes_published

    def get_recipe_not_published(self, request):
        recipes_not_published = Recipe.objects.filter(
            is_published=False,
            author=request.user
            )
        return recipes_not_published

    def render_dashboard(self, request, recipes_published,
                         recipes_not_published):
        return render(request, 'pages/dashboard.html', context={
            'recipes_published': recipes_published,
            'recipes_not_published': recipes_not_published,
            'number_recipes_published': len(recipes_published),
            'number_recipes_not_published': len(recipes_not_published),
            })

    def post(self, request):
        recipes_published = self.get_recipe_published(request)
        recipes_not_published = self.get_recipe_not_published(request)
        return self.render_dashboard(request, recipes_published,
                                     recipes_not_published)
