from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer
from tag.models import Tag


@api_view(http_method_names=['get', 'post'])
def recipe_api_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.filter(
            is_published=True
            ).order_by('-id').select_related(
                'category', 'author').prefetch_related(
                    'tags'
                )
        serializer = RecipeSerializer(instance=recipes, many=True, context={
            'request': request
        })
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()
        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED
        )


@api_view()
def recipe_api_detail(request, pk):
    recipes = get_object_or_404(
        Recipe.objects.filter(
            is_published=True
            ).order_by('-id'), pk=pk)
    serializer = RecipeSerializer(
        instance=recipes,
        many=False,
        context={
            'request': request
            })
    return Response(serializer.data)


@api_view()
def recipe_api_tag(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(), pk=pk)
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={
            'request': request
            })
    return Response(serializer.data)
