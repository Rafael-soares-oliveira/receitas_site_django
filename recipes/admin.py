from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from tag.models import Tag
from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    ...


class TagInLine(GenericStackedInline):
    model = Tag
    fields = 'name',
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_published',]
    list_display_links = ['title', 'created_at',]
    search_fields = ['title', 'description', 'slug', 'preparation_step',]
    list_filter = ['category', 'author', 'is_published',
                   'preparation_step_is_html',]
    list_editable = ['is_published',]
    ordering = ['-id',]
    prepopulated_fields = {
        "slug": ('title',)
    }
    list_per_page = 20
    inlines = [
        TagInLine,
    ]


admin.site.register(Category, CategoryAdmin)
