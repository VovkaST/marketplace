from django.urls import reverse_lazy
from django.views import generic

from app_import.forms import ImportForm
from app_import import tasks


class ImportView(generic.FormView):
    template_name = 'app_import/import.html'
    form_class = ImportForm
    success_url = reverse_lazy('import_data')

    def form_valid(self, form):
        form.instance.user = self.request.user
        protocol = form.save()
        tasks.import_file.delay(
            protocol_id=protocol.id,
            model_name=form.cleaned_data['target_model'],
            update=form.cleaned_data['update_data'],
        )
        return super().form_valid(form=form)
