from django.db import models
from django.contrib.auth.models import User
from time import time
from ckeditor_uploader.fields import RichTextUploadingField
from slugify import slugify


# creating slug
def gen_slug(string):
    finally_slug = slugify(string, allow_unicode=False,)
    return finally_slug + '-' + str(int(time()))


# model for Bulletin Board
class Board(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=False)
    text = models.TextField(blank=False)
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE, blank=False)
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL")
    images = RichTextUploadingField()  # upload to images in board
    video = RichTextUploadingField()  # upload to video in board

    def __str__(self):
        return f'{self.author} - {self.title} - {self.category}'

    def save(self, *args, **kwargs):
        # save in DB to slug
        self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        pass


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="slug")

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        # save in DB to slug
        self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        pass


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='response')
    board = models.ForeignKey('Board', on_delete=models.CASCADE,
                              related_name='response')

    def __str__(self):
        return f'{self.user} - {self.board}'

    def get_absolute_url(self):
        pass


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=False)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to='images/', null=True, blank=True)
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return f'{self.author} - {self.title}'

    def save(self, *args, **kwargs):
        # save in DB to slug
        self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)
