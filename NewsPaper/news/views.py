from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .models import Post, Category
from .filters import PostsFilter
from .forms import PostForm


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


class PostDetail(DetailView):
   model = Post
   template_name = 'detail.html'
   context_object_name = 'posts'
   
   
class PostCreateNews(ListView):
   model = Post
   template_name = 'create.html'
   context_object_name = 'posts'
   
def create_post(request):
    form = PostForm()    
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')
    
    return render(request, 'create.html', context={'form': form})
   
   
class PostEdit(ListView):
   model = Post
   template_name = 'edit.html'
   context_object_name = 'posts'
   

class PostDelete(ListView):
   model = Post
   template_name = 'delete.html'
   context_object_name = 'posts'
   
   
class PostsSearch(ListView):
   model = Post
   ordering = '-dateGreation'
   template_name = 'search.html'
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