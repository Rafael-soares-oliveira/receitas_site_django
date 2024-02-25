from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from authors.forms import BioFormEdit, MyProfileForm, ProfileFormEdit
from authors.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView)


class ProfileView(TemplateView):
    template_name = 'pages/profile.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        profile_id = context.get('id')
        profile = get_object_or_404(Profile.objects.filter(
            pk=profile_id,
        ).select_related('author'), pk=profile_id)
        return self.render_to_response(
            {
                **context,
                'profile': profile,
            }
        )


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
    )
class MyProfileView(UpdateView):
    template_name = 'pages/my_profile.html'
    form_class = MyProfileForm
    success_url = reverse_lazy('authors:myprofile_edit')

    def get_object(self):
        return self.request.user


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
    )
class BioEditView(UpdateView):
    template_name = 'pages/bio_edit.html'
    form_class = BioFormEdit
    success_url = reverse_lazy('authors:myprofile')

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, 'Your bio was update sucessfully.')
        return super(BioEditView, self).form_valid(form)


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
    )
class MyProfileEditView(UpdateView):
    template_name = 'pages/profile_edit.html'
    form_class = ProfileFormEdit
    success_url = reverse_lazy('authors:myprofile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your profile was update sucessfully.')
        return super().form_valid(form)


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
    )
class PasswordsChangeView(PasswordChangeView):
    success_url = reverse_lazy('authors:myprofile_edit_password')
    template_name = 'pages/change-password.html'
    success_url = reverse_lazy('authors:myprofile_edit_password_done')

    def form_valid(self, form):
        messages.success(self.request, 'Your password was update sucessfully.')
        return super().form_valid(form)


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
    )
class PasswordsDoneChangeView(PasswordChangeDoneView):
    template_name = 'pages/password-done.html'
