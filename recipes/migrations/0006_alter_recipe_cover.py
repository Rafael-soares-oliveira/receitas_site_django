# Generated by Django 5.0.1 on 2024-02-16 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_alter_recipe_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cover',
            field=models.ImageField(default='tests/tests_recipes/imagem_temporaria.jpg', upload_to='media/covers/%Y/%m/%d'),
        ),
    ]