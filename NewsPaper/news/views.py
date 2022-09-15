from django.shortcuts import render
from .models import Post

# Create your views here.
def index(request):
    post = Post.objects.all()
    return render(request, 'index.html', context={'post': post})

def detail(request, pk):
    post = Post.objects.get(pk__iexact=pk)
    return render(request, 'detail.html', context={'post': post})