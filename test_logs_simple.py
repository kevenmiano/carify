#!/usr/bin/env python3
"""
Script para testar logs no Loki
"""
import logging
import requests
import time

# Configurar logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_logs():
    print("Testando logs...")

    # Log de teste
    logger.info("TESTE: Log de teste para Loki", extra={
        'test': True,
        'service': 'carify-api-test',
        'timestamp': time.time()
    })

    # Fazer requisições para gerar logs
    try:
        response = requests.get("http://localhost:3000/health")
        logger.info(f"Health check: {response.status_code}")
    except Exception as e:
        logger.error(f"Erro no health check: {e}")

    print("Teste concluído!")

if __name__ == "__main__":
    test_logs()
