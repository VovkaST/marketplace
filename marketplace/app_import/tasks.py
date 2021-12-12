import json

from django.apps import apps
from django.db import transaction

from app_import.models import ImportProtocol
from marketplace import celery_app

APPS_MAP = {
    'sellers': ('app_sellers', 'Sellers'),
    'goods': ('app_sellers', 'Goods'),
    'goods_descriptions': ('app_sellers', 'GoodsDescriptionsValues'),
}


class ImportFileTask(celery_app.Task):
    def on_success(self, retval, task_id, args, kwargs):
        protocol_id = kwargs['protocol_id']
        ImportProtocol.objects.filter(id=protocol_id).update(is_imported=True, result=json.dumps(retval))


@celery_app.task(bind=True, base=ImportFileTask)
def import_file(self, protocol_id: int, model_name: str, update: bool, delimiter: str) -> dict:
    total, created, updated = 0, 0, 0
    errors = list()
    protocol = ImportProtocol.objects.get(id=protocol_id)
    app, class_name = APPS_MAP[model_name]

    model = apps.get_model(app_label=app, model_name=class_name)
    with open(file=protocol.filename.path, encoding='utf-8', mode='r') as datafile:
        headers = next(datafile).split(delimiter)
        with transaction.atomic():
            for row_number, row in enumerate(datafile, start=2):
                obj = model()
                data = dict(zip(headers, row.split(delimiter)))
                obj.set_values(data=data)

                n_key = obj.natural_key()
                obj_in_db = model.objects.get_by_natural_key(**n_key)
                if obj_in_db and update:
                    obj = obj_in_db.set_values(data=data)
                    updated += 1
                if not obj_in_db or (obj_in_db and update):
                    try:
                        obj.save()
                        created += 1
                    except Exception as exc:
                        errors.append({
                            'error': exc.args[0],
                            'row_number': row_number,
                        })
                total += 1
    protocol.total_objects = total
    protocol.new_objects = created
    protocol.task_id = self.request.id
    protocol.save(force_update=True, update_fields=['is_imported', 'total_objects', 'new_objects', 'task_id'])
    return {
        'success': not bool(errors),
        'errors': errors,
        'total': total,
        'created': created,
        'updated': updated,
    }
