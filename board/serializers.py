from .models import Board, Category, ResponseBoard, Post
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
        ]


class BoardSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Board
        fields = [
            'id',
            'author',
            'title',
            'text',
            'category',
            'slug',
            'image',
            'video',
        ]


class CategorySerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
        ]


class ResponseSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ResponseBoard
        fields = [
            'id',
            'user',
            'board'
        ]


class PostSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'title',
            'text',
            'created_date',
            'slug',
            'image',
        ]
