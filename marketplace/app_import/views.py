from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from app_import.forms import ImportForm
from app_import import tasks


class ImportView(LoginRequiredMixin, generic.FormView):
    template_name = 'app_import/import.html'
    form_class = ImportForm
    success_url = reverse_lazy('import_data')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        protocol = form.save()
        tasks.import_file.delay(
            protocol_id=protocol.id,
            model_name=form.cleaned_data['target_model'],
            update=form.cleaned_data['update_data'],
            delimiter=form.cleaned_data['delimiter'],
        )
        return super().form_valid(form=form)
