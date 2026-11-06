from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import CustomUserCreationForm, ProfileUpdateForm


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    success_message = 'Your account has been created. You can now log in.'


class ProfileUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('dashboard')
    success_message = 'Your profile has been updated.'

    def get_object(self, queryset=None):
        return self.request.user
