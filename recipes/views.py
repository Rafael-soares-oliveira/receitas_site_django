from django.shortcuts import render, get_list_or_404, get_object_or_404
from recipes.models import Recipe
# Create your views here.


def home(request):
    recipe = Recipe.objects.filter(
        is_published=True).order_by('-id')

    return render(request, 'pages/home.html', context={
        'recipes': recipe,
    })


def recipe(request):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(request, 'pages/recipe-view.html',
                  context={
                      'recipe': recipe,
                      'is_detail_page': True,
                  })
