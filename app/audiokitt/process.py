from django_rq import job

from .pipeline import Pipeline


def run_processing_pipeline(instance):
    return pipeline_task.delay(instance)


@job
def pipeline_task(instance):
    from .models import Analyse

    p = Pipeline(instance.file.path)

    try:
        instance.analyse_data = p.run()
        instance.status = Analyse.STATUS_DONE
    except Exception as e:
        print(e)
        instance.status = Analyse.STATUS_ERROR

    instance.save()
