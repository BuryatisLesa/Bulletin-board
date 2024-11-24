from django.contrib import admin
from .models import (
    Board, Category, ResponseBoard, Post,
)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category')
    fields = ('author', 'title', 'text', 'category', 'image', 'video')


admin.site.register(Category)
admin.site.register(ResponseBoard)
admin.site.register(Post)
