from django.http import Http404
from recipes.models import Recipe
from django.db.models import Q
from utils.make_pagination import make_pagination
import os
from django.views.generic import ListView, DetailView
# Create your views here.

PER_PAGE = os.environ.get('PER_PAGE', 10)


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )
        ctx.update(
            {'recipes': page_obj, 'pagination_range': pagination_range,
             'last_page': pagination_range['total_pages'],
             }
        )
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = "pages/home.html"


class RecipeListViewCategory(RecipeListViewBase):
    template_name = "pages/category-view.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
            category__id=self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404()

        return qs


class RecipeListViewSearch(RecipeListViewBase):
    template_name = "pages/search-view.html"

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()

        if not search_term:
            raise Http404()

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
                ),
            is_published=True,
            )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )
        ctx.update(
            {'recipes': page_obj,
             'pagination_range': pagination_range,
             'last_page': pagination_range['total_pages'],
             'additional_url_query': f'?q={search_term}',
             'title': f'Search for "{search_term}" | ',
             'search_term': search_term,
             }
        )
        return ctx


class RecipeDetail(DetailView):
    model = Recipe
    template_name = "pages/recipe-view.html"
    context_object_name = 'recipe'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )

        if not qs:
            raise Http404()

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'is_detail_page': True,
        })
        return ctx
