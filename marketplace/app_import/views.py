import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic

from app_import.forms import ImportForm
from app_import.models import ImportProtocol
from app_import import tasks
from main.views import CategoryMixin, PageInfoMixin


class ImportView(CategoryMixin, PageInfoMixin, LoginRequiredMixin, generic.FormView):
    template_name = 'app_import/import.html'
    form_class = ImportForm
    success_url = reverse_lazy('import_data')
    page_title = _('Import data')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        protocols = ImportProtocol.objects.active_tasks(user=self.request.user).order_by('-created_at')
        context = super().get_context_data(**kwargs)
        context.update({
            'import_tasks': [
                {
                    'uuid': protocol.task_id,
                    'result': json.loads(protocol.result or '""'),
                    'date': protocol.created_at,
                }
                for protocol in protocols
            ],
        })
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        protocol = form.save()

        task_kwargs = {
            'protocol_id': protocol.id,
            'model_name': form.cleaned_data['target_model'],
            'update': form.cleaned_data['update_data'],
            'delimiter': form.cleaned_data['delimiter'],
        }
        tasks.import_file.delay(**task_kwargs)
        return super().form_valid(form=form)


class TaskCheckView(LoginRequiredMixin, generic.View):
    def post(self, request):
        error = None
        uuids = request.POST.getlist('uuid[]')
        tasks = [
            {
                'uuid': task['task_id'],
                'success': task['is_imported'],
                'total': task['total_objects'] if task['is_imported'] else None,
                'created': task['new_objects'] if task['is_imported'] else None,
                'updated': task['updated_objects'] if task['is_imported'] else None,
            }
            for task in ImportProtocol.objects.tasks_results(user=request.user, tasks=uuids)
        ]
        return JsonResponse({
            'success': bool(tasks),
            'error': error,
            'tasks': tasks
        })

