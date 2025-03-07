from otel_wrapper import OpenObservability

metrics_wrapper = OpenObservability(application_name="currency-quote").get_wrapper().metrics()


def increment_metric(func):
    def inner(*args, **kwargs):
        metrics_wrapper.metric_increment(func.__qualname__, value=1, tags=kwargs)
        return func(*args, **kwargs)
    return inner
