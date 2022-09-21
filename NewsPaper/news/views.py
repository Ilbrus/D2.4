from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


# Create your views here.
class PostsList(ListView):
   model = Post
   ordering = '-dateGreation'
   template_name = 'index.html'
   context_object_name = 'posts'
   paginate_by = 2  

#def index(request):
#    #posts = Post.objects.all()
#    posts = Post.objects.order_by('-dateGreation')
#    paginate_by = 2 
#    return render(request, 'index.html', context={'posts': posts})
#        
#def detail(request, pk):
#    post = Post.objects.get(pk__iexact=pk)
#    paginate_by = 2 
#    return render(request, 'detail.html', context={'post': post})