from functools import wraps
from otel_wrapper.deps_injector import wrapper_builder

telemetry = wrapper_builder("currency-quote")
metrics_wrapper = telemetry.metrics()
traces_wrapper = telemetry.traces()


def increment_metric(func):
    @wraps(func)
    def inner(*args, **kwargs):
        metrics_wrapper.metric_increment(name=func.__qualname__, value=1.0, tags=kwargs)
        return func(*args, **kwargs)
    return inner


def trace_span(func):
    @wraps(func)
    def inner(*args, **kwargs):
        # Create a new span
        span = traces_wrapper.new_span(func.__qualname__)
        
        try:
            # Add attributes to the span from kwargs
            for key, value in kwargs.items():
                if isinstance(value, (str, int, float, bool)):
                    span.set_attribute(f"{key}", value)
            
            # Execute the function
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            span.record_exception(e)
            raise
        finally:
            span.end()
    return inner


# Helper function to inject context into HTTP headers
def inject_context_into_headers(headers=None):
    if headers is None:
        headers = {}
    traces_wrapper.inject_context_into_headers(headers)
    return headers


# Helper function to extract context from HTTP headers
def extract_context_from_headers(headers):
    return traces_wrapper.extract_context_from_headers(headers)
