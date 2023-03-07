from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from .filters import PostFilter
from .forms import PostForm
from .models import *
from datetime import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


class PostNewsList(ListView):
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # queryset = Post.objects.order_by(
    #     categoryType_lt='NW',
    # )

    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostNewsDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class PostSearch(ListView):
    form_class = PostForm
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'post_search'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('appnews.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    # def form_valid(self, form):
    #     category = form.save(commit=False)
    #     category.categoryType = 'AR'
    #     return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('appnews.update_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_update')


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('appnews.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('start_new')

