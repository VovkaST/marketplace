from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class ImportProtocol(models.Model):
    filename = models.FileField(_('Data file path'), upload_to='files/import/')
    is_imported = models.BooleanField(_('Import mark'), default=False)
    total_objects = models.IntegerField(_('Total objects quantity'), default=0)
    new_objects = models.IntegerField(_('New objects quantity'), default=0)
    user = models.ForeignKey(User, verbose_name=_('Imported by'), on_delete=models.CASCADE, related_name='imported_by')
    created_at = models.DateTimeField(_('Creation date, time'), auto_created=True)

    class Meta:
        db_table = 'mp_import_protocol'
        verbose_name = _('Import data protocol')
        verbose_name_plural = _('Import data protocols')

    def __str__(self):
        is_loaded = _('Loaded') if self.is_imported else _('Not loaded')
        return mark_safe(f'"{self.filename.path}" &ndash; {self.total_objects}/{self.new_objects} ({is_loaded})')
