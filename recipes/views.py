from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from recipes.models import Recipe
from django.db.models import Q
from utils.make_pagination import make_pagination
import os
# Create your views here.

PER_PAGE = int(os.environ.get('PER_PAGE', 10))


def home(request):
    recipe = Recipe.objects.filter(
        is_published=True).order_by('-id')

    page_object, pagination_range = make_pagination(request, recipe, PER_PAGE)

    return render(request, 'pages/home.html', context={
        'recipes': page_object,
        'pagination_range': pagination_range,
        'last_page': pagination_range['total_pages']
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

    page_object, pagination_range = make_pagination(request, recipe, PER_PAGE)

    return render(request, 'pages/category-view.html', context={
        'recipes': page_object,
        'pagination_range': pagination_range,
        'last_page': pagination_range['total_pages'],
        'title': f'{recipe[0].category.name} | '  # type:ignore
    })


def search(request):
    search_term = request.GET.get('q', '').strip()
    recipe = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term), is_published=True)
        ).order_by('-id')

    if not search_term:
        raise Http404

    page_object, pagination_range = make_pagination(request, recipe, PER_PAGE)

    return render(request, 'pages/search-view.html', {
        'title': f'Search for "{search_term}" | ',
        'search_term': search_term,
        'recipes': page_object,
        'additional_url_query': f'&q={search_term}',
        'pagination_range': pagination_range,
        'last_page': pagination_range['total_pages'],
    })
