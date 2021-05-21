from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .utils import *


class PhysicistsHome(DataMixin, ListView):
    model = Physicists
    template_name = 'famous_physicists/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Main page')
        all_context = context | c_def
        return all_context

    def get_queryset(self):
        return Physicists.objects.filter(is_published=True).select_related('cat')


class AddArticle(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'famous_physicists/add_article.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('sign_in')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add article')
        all_context = context | c_def
        return all_context


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'famous_physicists/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Feedback')
        all_context = context | c_def
        return all_context

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class ShowPost(DataMixin, DetailView):
    model = Physicists
    template_name = 'famous_physicists/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'], cat_selected=context['post'].cat_id)
        all_context = context | c_def
        return all_context


class PhysicistsCategory(DataMixin, ListView):
    model = Physicists
    template_name = 'famous_physicists/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Physicists.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Category - ' + str(c.research_area),
                                      cat_selected=c.pk)
        all_context = context | c_def
        return all_context


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'famous_physicists/sign_up.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RegisterUser, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Sign up')
        all_context = context | c_def
        return all_context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class SignInUser(DataMixin, LoginView):
    form_class = SignInUserForm
    template_name = 'famous_physicists/sign_in.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Sign in')
        all_context = context | c_def
        return all_context

    def get_success_url(self):
        return reverse_lazy('home')


class About(DataMixin, TemplateView):
    template_name = 'famous_physicists/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='About')
        all_context = context | c_def
        return all_context


def logout_user(request):
    logout(request)
    return redirect('sign_in')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Sorry, page not found</h1>')
