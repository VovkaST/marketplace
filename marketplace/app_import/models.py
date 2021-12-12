from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from marketplace.settings import IMPORT_UPLOAD_DIR
from services.validators import FileValidator


class ImportProtocol(models.Model):
    filename = models.FileField(
        _('Data file path'),
        upload_to=IMPORT_UPLOAD_DIR,
        validators=[FileValidator(allowed_extensions=['csv'])]
    )
    task_id = models.CharField(_('Celery task id'), max_length=36)
    result = models.CharField(_('Task execution result'), max_length=2000)
    is_imported = models.BooleanField(_('Import mark'), default=False)
    total_objects = models.IntegerField(_('Total objects quantity'), default=0)
    new_objects = models.IntegerField(_('New objects quantity'), default=0)
    user = models.ForeignKey(
        User,
        verbose_name=_('Imported by'),
        on_delete=models.CASCADE,
        related_name='imported_by'
    )
    created_at = models.DateTimeField(_('Creation date, time'), auto_now_add=True)

    class Meta:
        db_table = 'mp_import_protocol'
        verbose_name = _('Import data protocol')
        verbose_name_plural = _('Import data protocols')

    def __str__(self):
        is_loaded = _('Loaded') if self.is_imported else _('Not loaded')
        return mark_safe(f'"{self.filename.path}" &ndash; {self.total_objects}/{self.new_objects} ({is_loaded})')
