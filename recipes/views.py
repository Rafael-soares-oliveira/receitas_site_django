from django.shortcuts import render, get_list_or_404, get_object_or_404
from recipes.models import Recipe
# Create your views here.


def home(request):
    recipe = Recipe.objects.filter(
        is_published=True).order_by('-id')

    return render(request, 'pages/home.html', context={
        'recipes': recipe,
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(request, 'pages/recipe-view.html',
                  context={
                      'recipe': recipe,
                      'is_detail_page': True,
                  })


def category(request, category_id):
    recipe = get_list_or_404(Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id'))
    return render(request, 'pages/category-view.html', context={
        'recipes': recipe,
        'title': f'{recipe[0].category.name} | '  # type:ignore
    })
