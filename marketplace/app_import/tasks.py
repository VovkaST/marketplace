from marketplace import celery_app


@celery_app.task
def import_file(protocol_id):
    pass
