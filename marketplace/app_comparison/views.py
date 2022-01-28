from django.http import JsonResponse
from django.views import generic
from django.utils.translation import gettext_lazy as _

from app_comparison.forms import ComparisonForm
from main.views import CacheSettingsMixin, CategoryMixin, PageInfoMixin
from services.comparison import get_comparison_context
from services.goods import comparison_good_add, comparison_good_remove


class ComparisonView(CategoryMixin, PageInfoMixin, CacheSettingsMixin, generic.TemplateView):
    page_title = _('Goods comparison')
    template_name = 'app_comparison/comparison.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user if self.request.user.is_authenticated else None
        context.update(get_comparison_context(user=user, session=self.request.session.session_key))
        context.update({
            'cache_key': user.username if user else self.request.session.session_key,
        })
        return context


class ComparisonAddView(generic.FormView):
    form_class = ComparisonForm

    def form_valid(self, form):
        obj_data = {
            'good_id': form.cleaned_data.get('good_id'),
            'user': self.request.user if self.request.user.is_authenticated else None,
            'session': self.request.session.session_key,
        }
        data, error = comparison_good_add(**obj_data)
        return JsonResponse({
            'success': not error,
            'error': error,
            **data
        })


class ComparisonRemoveView(generic.FormView):
    form_class = ComparisonForm

    def form_valid(self, form):
        obj_data = {
            'good_id': form.cleaned_data.get('good_id'),
            'user': self.request.user if self.request.user.is_authenticated else None,
            'session': self.request.session.session_key,
        }
        data, error = comparison_good_remove(**obj_data)
        return JsonResponse({
            'success': not error,
            'error': error,
            **data
        })
