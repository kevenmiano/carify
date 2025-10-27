import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.trace import Status, StatusCode
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_telemetry(app):
    resource = Resource.create({
        "service.name": os.getenv("SERVICE_NAME", "carify-api"),
        "service.version": os.getenv("SERVICE_VERSION", "0.1.0"),
        "deployment.environment": os.getenv("ENVIRONMENT", "production"),
    })

    trace_provider = TracerProvider(resource=resource)
    otlp_endpoint = os.getenv("OTLP_ENDPOINT", "http://localhost:4317")
    otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    trace_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    trace.set_tracer_provider(trace_provider)

    log_provider = LoggerProvider(resource=resource)
    set_logger_provider(log_provider)

    log_exporter = OTLPLogExporter(endpoint=otlp_endpoint, insecure=True)
    log_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

    handler = LoggingHandler(logger_provider=log_provider)
    logging.getLogger().addHandler(handler)

    FlaskInstrumentor().instrument_app(app)

    logger.info(f"OpenTelemetry configured: {otlp_endpoint}")
    logger.info(f"Service name: {resource.attributes.get('service.name')}")
    logger.info(f"Service version: {resource.attributes.get('service.version')}")
    logger.info(f"Environment: {resource.attributes.get('deployment.environment')}")

    return trace.get_tracer(__name__)


def trace_exception(tracer, exception: Exception, context: dict = None):
    with tracer.start_as_current_span("exception_handler") as span:
        span.set_status(Status(StatusCode.ERROR, str(exception)))
        span.set_attribute("exception.type", type(exception).__name__)
        span.set_attribute("exception.message", str(exception))

        if hasattr(exception, 'status_code'):
            span.set_attribute("http.status_code", exception.status_code)

        if context:
            for key, value in context.items():
                span.set_attribute(f"context.{key}", str(value))

        span.record_exception(exception)

        logger.error(
            f"Exception: {type(exception).__name__} - {str(exception)}",
            extra={"exception_type": type(exception).__name__, "context": context},
            exc_info=True
        )
