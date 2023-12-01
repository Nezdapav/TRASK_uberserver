from typing import Callable

from prometheus_client import Counter, Histogram
from prometheus_fastapi_instrumentator.metrics import Info

errors_total = Counter(
    "errors_total",
    "Errors occurred during runtime.",
    ("app", "type", "endpoint"),
)

request_duration_seconds_hist = Histogram(
    "request_duration_seconds",
    "Histogram of uberserver requests duration in seconds.",
    ("app", "endpoint", "status_code", "method"),
)


def increment_errors_total(exception_name: str, endpoint: str) -> None:
    """Increment errors_total metric."""
    errors_total.labels("uberserver", exception_name, endpoint).inc()


def request_duration_seconds() -> Callable[[Info], None]:
    def instrumentation(info: Info) -> None:
        request_duration_seconds_hist.labels(
            "uberserver",
            info.modified_handler,
            info.modified_status,
            info.request.method,
        ).observe(info.modified_duration)

    return instrumentation
