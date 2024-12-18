from django.db import models
from django.contrib.auth.models import User
from time import time
from slugify import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


# creating slug
def gen_slug(string):
    finally_slug = slugify(string, allow_unicode=False,)
    return finally_slug + '-' + str(int(time()))


# model for Bulletin Board
class Board(models.Model):
    '''fields =[author, title, text,
    category, created_date, slug, image, video]'''
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=False)
    text = RichTextUploadingField()
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE, blank=False)
    created_date = models.DateTimeField(auto_now_add=True, null=True,
                                        blank=True)
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL",
        blank=True)
    image = models.ImageField(
        upload_to='boards/images/', null=True, blank=True,
        default='boards/images/default_image.jpg')  # upload to images in board
    video = models.FileField(
        upload_to='boards/videos',
        null=True, blank=True)   # upload to video in board

    def __str__(self):
        return f'{self.author} - {self.title} - {self.category}'

    def save(self, *args, **kwargs):
        # save in DB to slug
        self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('BoardDetail', kwargs={'slug':
                                              self.slug, 'pk': self.pk})


class Category(models.Model):
    '''fields = [name, slug, descriptions, image]'''
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=150)
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL",
        blank=True)
    descriptions = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='categories/images/', null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('CategoryDetail', kwargs={'slug':
                                                 self.slug, 'pk': self.pk})

    def save(self, *args, **kwargs):
        # save in DB to slug
        self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)


class ResponseBoard(models.Model):
    '''fields = [user, board]'''
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='response')
    board = models.ForeignKey('Board', on_delete=models.CASCADE,
                              related_name='responseboard')
    is_accept = models.BooleanField(default=0)

    def __str__(self):
        return f'{self.user} - {self.board}'

    def get_absolute_url(self):
        return reverse('PageResponses',
                       kwargs={'slug': self.slug, 'pk': self.pk})


class Post(models.Model):
    '''fields = [author, title, text, created_date, image, video, slug]'''
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=False)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to='posts/images/', null=True, blank=True)
    video = models.FileField(
        upload_to='posts/videos', null=True, blank=True)

    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL",
        blank=True)

    def __str__(self):
        return f'{self.author} - {self.title}'

    def get_absolute_url(self):
        return reverse('PostDetail', kwargs={'slug': self.slug, 'pk': self.pk})

    def save(self, *args, **kwargs):
        # save in DB to slug
        self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)
