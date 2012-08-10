from celery.task import task #@UnresolvedImport

@task(ignore_result=True)
def test_task():
    pass