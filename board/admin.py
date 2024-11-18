from django.contrib import admin
from .models import (
    Board,
    Category,
    Response,
    Post,
)

admin.site.register(Board)
admin.site.register(Category)
admin.site.register(Response)
admin.site.register(Post)
