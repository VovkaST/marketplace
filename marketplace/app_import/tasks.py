from importlib import import_module

from app_import.models import ImportProtocol
from marketplace import celery_app


@celery_app.task
def import_file(protocol_id: int, model_name: str):
    protocol = ImportProtocol.objects.get(id=protocol_id)
    apps = {
        'sellers': ('app_sellers.models', 'Sellers'),
        'goods': ('app_sellers.models', 'Goods'),
    }
    package, class_name = apps[model_name]
    try:
        imported = import_module(package)
    except ModuleNotFoundError:
        # todo: Ошибка импорта
        return

    model = getattr(imported, class_name)
    obj = model()
    with open(file=protocol.filename.path, encoding='utf-8', mode='r') as datafile:
        headers = []
        for row in datafile:
            if not headers:
                headers = row.split(';')
                continue
            for field_name, value in dict(zip(headers, row.split(';'))).items():
                setattr(obj, field_name, value)
            obj.save()
    pass
