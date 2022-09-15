from django.shortcuts import render
from .models import Post
from django.views.generic import ListView

# Create your views here.
def index(request):
    #posts = Post.objects.all()
    posts = Post.objects.order_by('-dateGreation')
    return render(request, 'index.html', context={'posts': posts})

def detail(request, pk):
    post = Post.objects.get(pk__iexact=pk)
    return render(request, 'detail.html', context={'post': post})