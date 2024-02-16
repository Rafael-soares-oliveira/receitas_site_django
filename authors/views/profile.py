from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from authors.forms import MyProfileForm, ProfileForm
from authors.models import Profile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm


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
class MyProfileEditView(UpdateView):
    template_name = 'pages/profile_edit.html'
    form_class = ProfileForm

    def get_object(self):
        return self.request.user


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
    )
class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('authors:myprofile')
