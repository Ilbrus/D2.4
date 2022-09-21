from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category
from .filters import PostsFilter


# Create your views here.
class PostsList(ListView):
   model = Post
   ordering = '-dateGreation'
   template_name = 'index.html'
   context_object_name = 'posts'
   paginate_by = 10  
   
   # Переопределяем функцию получения списка товаров
   def get_queryset(self):
       # Получаем обычный запрос
       queryset = super().get_queryset()
       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict, который мы рассматривали
       # в этом юните ранее.
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне.
       self.filterset = PostsFilter(self.request.GET, queryset)
       # Возвращаем из функции отфильтрованный список товаров
       return self.filterset.qs

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Добавляем в контекст объект фильтрации.
       context['filterset'] = self.filterset
       return context


class PostsDetail(DetailView):
   model = Post
   template_name = 'detail.html'
   context_object_name = 'posts'
   
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