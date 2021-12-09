from pathlib import Path

from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileValidator:
    error_messages = {
        'max_size': (_("Ensure this file size is not greater than %(max_size)s."
                     " Your file size is %(size)s.")),
        'file_type': _('File extension “%(extension)s” is not allowed. '
                       'Allowed extensions are: %(allowed_extensions)s.'),
    }

    def __init__(self, allowed_extensions: list = None, max_size: int = None):
        if allowed_extensions is not None:
            allowed_extensions = [allowed_extension.lower() for allowed_extension in allowed_extensions]
        self.allowed_extensions = allowed_extensions
        self.max_size = max_size

    def __call__(self, field_file):
        if isinstance(self.max_size, int) and field_file.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(field_file.size),
            }
            raise ValidationError(self.error_messages['max_size'],
                                  'max_size', params)
        file_name = Path(field_file.name).suffix
        extension = file_name[1:].lower()
        if self.allowed_extensions is not None and extension not in self.allowed_extensions:
            raise ValidationError(
                self.error_messages['file_type'],
                code='file_type',
                params={
                    'extension': extension,
                    'allowed_extensions': ', '.join(self.allowed_extensions),
                }
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.allowed_extensions == other.allowed_extensions and
            self.max_size == other.max_size
        )
