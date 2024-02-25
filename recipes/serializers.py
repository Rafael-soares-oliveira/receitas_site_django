from rest_framework import serializers
from recipes.models import Recipe
from tag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'preparation', 'servings',
            'preparation_step', 'category', 'author', 'tag_objects',
            'tag_links',
            ]

    preparation = serializers.SerializerMethodField(read_only=True,)
    servings = serializers.SerializerMethodField(read_only=True,)
    category = serializers.StringRelatedField(read_only=True,)
    author = serializers.SerializerMethodField(read_only=True,)
    tag_objects = TagSerializer(many=True, source='tags', read_only=True)
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:recipes_api_v2_tag',
        read_only=True,
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def get_servings(self, recipe):
        return f'{recipe.servings} {recipe.servings_unit}'

    def get_author(self, recipe):
        return f'{recipe.author.id} - {recipe.author}'

    def validate(self, attrs):
        super_validate = super().validate(attrs)

        title = attrs.get('title')
        description = attrs.get('description')

        if title == description:
            raise serializers.ValidationError(
                {
                    "title": ["Posso", "ter", "mais de um erro"],
                    "description": ["Posso", "ter", "mais de um erro"],
                }
            )

        return super_validate

    def validate_title(self, value):
        title = value

        if len(title) < 5:
            raise serializers.ValidationError('Must have at least 5 chars.')

        return title
