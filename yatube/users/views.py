from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm

# Create your views here.


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'
