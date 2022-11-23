from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostsFilter
from .forms import PostForm, ProfileUserForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
import logging

logger = logging.getLogger(__name__)

def index(request):
    logger.info('INFO')
    posts = Post.object.all()
    return render(request, 'index.html', context={'news': news})   


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
   context_object_name = 'post'
   
   
   
class PostCreateNews(CreateView):
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
   
   
class PostEdit(UpdateView):
   form_class = PostForm
   model = Post
   template_name = 'edit.html'
   

class PostDelete(DeleteView):
   model = Post
   template_name = 'delete.html'
   context_object_name = 'post'
   success_url = reverse_lazy('post_list')
   
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
   
class ProfileUserUpdate(UpdateView):
    model = User
    form_class = ProfileUserForm
    template_name = 'profile_edit.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('profile_user_update')
    

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'
    

class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'
    
    
    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-dateGreation')
        return queryset
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['postCategory'] = self.postCategory
        return context


#@LoginRequiredMixin
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    
    
    message = 'Вы успешно подписались ...'
    return render(request, 'subscribe.html', {'category': category, 'message': message})