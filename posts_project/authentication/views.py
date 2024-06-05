from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from authentication import models, forms
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView, PasswordChangeView
from django.urls import reverse_lazy


class LoginView(LoginView):
    redirect_authenticated_user = True
    template_name='authentication/login.html'

    def get_success_url(self):
        return reverse_lazy('index')

    def form_invalid(self, form):
        messages.error(self.request,'Неправильный логин или пароль')
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(LogoutView):
    next_page = reverse_lazy('login')


class RegistrationView(CreateView):
    template_name = "authentication/registration.html"
    model = models.CustomUser
    form_class = forms.UserRegistrationForm
    success_url = reverse_lazy("registration_successful")

    def form_invalid(self, form):
        messages.error(self.request,'Неправильный логин или пароль')
        return self.render_to_response(self.get_context_data(form=form))


class RegistrationSuccessfulView(TemplateView):
    template_name = "authentication/registration_successful.html"


class PasswordResetView(PasswordResetView):
    template_name = 'authentication/password/password_reset_form.html'  # Кастомная страница ввода email
    email_template_name = 'authentication/password/password_reset_email.html'  # Кастомный шаблон email
    success_url = reverse_lazy('password_reset_done')

    # subject_template_name = 'auth/password/password_reset_email.txt'


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'authentication/password/password_reset_confirm_form.html'  # Кастомная страница ввода нового пароля
    success_url = reverse_lazy('password_reset_complete')
    # reset_url_token = 'set-password'


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'authentication/password/password_reset_done.html'  # Кастомная страница ввода нового пароля


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'authentication/password/password_reset_complete.html'


class UserProfileView(UpdateView):
    model = models.CustomUser
    queryset = models.CustomUser.objects.all()
    form_class = forms.UserProfileForm
    template_name = 'authentication/profile.html'

    def get_success_url(self) -> str:
        success_url = '/account/profile/%s'%self.get_object().pk

        return success_url
