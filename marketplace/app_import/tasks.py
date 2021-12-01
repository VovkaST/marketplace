from importlib import import_module

from app_import.models import ImportProtocol
from marketplace import celery_app


APPS_MAP = {
    'sellers': 'app_sellers',
    'goods': 'app_sellers',
}


@celery_app.task
def import_file(protocol_id: int, model_name: str, update: bool):
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
    with open(file=protocol.filename.path, encoding='utf-8', mode='r') as datafile:
        headers = next(datafile).split(';')
        for row in datafile:
            obj = model()
            data = dict(zip(headers, row.split(';')))
            obj.set_values(data=data)

            n_key = obj.natural_key()
            obj_in_db = model.objects.get_by_natural_key(**n_key)
            if obj_in_db and update:
                obj = obj_in_db.set_values(data=data)
            if not obj_in_db or (obj_in_db and update):
                obj.save()

    return True
