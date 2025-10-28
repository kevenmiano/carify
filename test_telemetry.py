#!/usr/bin/env python3
"""
Script para testar OpenTelemetry e logs
"""
import os
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter as OTLPLogExporterHTTP

# Configurar logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_telemetry():
    print("Iniciando teste de OpenTelemetry...")
    
    # Configurar resource
    resource = Resource.create({
        "service.name": "carify-api-test",
        "service.version": "0.1.0",
        "deployment.environment": "test",
    })
    
    # Configurar Tracing
    trace_provider = TracerProvider(resource=resource)
    otlp_endpoint = "http://localhost:4317"
    otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    trace_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    trace.set_tracer_provider(trace_provider)
    
    # Configurar Logging
    log_provider = LoggerProvider(resource=resource)
    set_logger_provider(log_provider)
    
    # Exportar logs via OTLP HTTP
    log_exporter = OTLPLogExporterHTTP(endpoint="http://localhost:4318/v1/logs")
    log_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    
    # Configurar handler para logs estruturados
    handler = LoggingHandler(logger_provider=log_provider)
    logging.getLogger().addHandler(handler)
    
    print("OpenTelemetry configurado!")
    
    # Gerar alguns logs de teste
    logger.info("TESTE: Log de teste 1", extra={
        'test': True,
        'service': 'carify-api-test',
        'level': 'info'
    })
    
    logger.warning("TESTE: Log de warning", extra={
        'test': True,
        'service': 'carify-api-test',
        'level': 'warning'
    })
    
    logger.error("TESTE: Log de erro", extra={
        'test': True,
        'service': 'carify-api-test',
        'level': 'error'
    })
    
    # Gerar um span de teste
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("test_span") as span:
        span.set_attribute("test.attribute", "test_value")
        span.set_attribute("service.name", "carify-api-test")
        
        logger.info("TESTE: Log dentro do span", extra={
            'test': True,
            'span_id': span.get_span_context().span_id,
            'trace_id': span.get_span_context().trace_id
        })
    
    print("Teste concluído! Verifique os logs no Grafana/Loki")
    print("Query sugerida: {service_name=\"carify-api-test\"}")

if __name__ == "__main__":
    test_telemetry()


