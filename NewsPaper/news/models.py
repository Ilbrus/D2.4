from cgitb import text
from tkinter import CASCADE
from turtle import title
from unicodedata import category, name
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat *3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')
    
    def __str__(self):
        return f'{self.name}'

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    ordering = '-dateCreation'
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateGreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)


    def get_absolute_url(self):
        #rreturn f'/news/{self.pk}'
        #return reverse( '/news/' , kwargs={"pk": self.pk})
        return reverse('post_detail', args=[str(self.pk)])
    
    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'    


class PostCategory(models.Model):
    postThrought = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrought = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateGreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)
    

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
        
        
class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username", 
                  "first_name", 
                  "last_name", 
                  "email", 
                  "password1", 
                  "password2", )