from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from authors.models import Profile


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
    )
class ProfileView(TemplateView):
    template_name = 'pages/profile.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        profile_id = context.get('id')
        return self.render_to_response(
            {
                **context,
            }
        )
