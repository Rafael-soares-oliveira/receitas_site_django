from django.contrib import admin
from .models import Category, Recipe

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    ...


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


admin.site.register(Category, CategoryAdmin)
